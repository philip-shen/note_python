# Python PySimpleGUIで作るPDFリーダー
# https://qlitre-weblog.com/pysimplegui-pdf-reader/

import fitz
import PySimpleGUI as sg

class GuiFrontend:
    """GUIの見た目を定義"""

    def __init__(self):
        self.title = 'PDF Reader'

    @staticmethod
    def frame_zoom_control():
        """zoom制御のフレームを返す"""
        btn_size = (6, 1)
        return sg.Frame(title='Zoom Control',
                        layout=[
                            [sg.Button('Clear', size=(10, 1))],
                            [sg.Button('Top-L', size=btn_size), sg.Button('Top-R', size=btn_size)],
                            [sg.Button('Bot-L', size=btn_size), sg.Button('Bot-R', size=btn_size), ]
                        ])

    @staticmethod
    def left_col():
        """左側のcolumnを返す"""
        accepted_file_types = (("PDF Files", "*.pdf"),)

        return sg.Column(layout=[
            [sg.Text("PDF"),
             sg.InputText(key='DOC_NAME', enable_events=True),
             sg.FileBrowse(key="PDF", file_types=accepted_file_types),
             sg.InputText("1", size=(3, 1), key='GOTO'),
             sg.T('/', key='TOTAL_PAGE'),
             sg.Button('GO', key='GO')],
            [sg.Image(data=None, key='IMAGE')],
        ], vertical_alignment='t')

    def right_col(self):
        """右側のcolumnを返す"""

        return sg.Column(layout=[
            [sg.Button('Prev'), sg.Button('Next')],
            [self.frame_zoom_control()]
        ], vertical_alignment='t')

    def layout(self):
        """レイアウトを返す"""
        return [
            [self.left_col(), sg.VSeparator(), self.right_col()]
        ]

    def window(self):
        """windowを返す"""
        return sg.Window(title=self.title,
                         layout=self.layout(),
                         return_keyboard_events=True,
                         use_default_focus=False,
                         size=(1000, 800),
                         resizable=True,
                         finalize=True)


class GuiBackend:
    """
    GUIの機能面を提供
    """

    def __init__(self):
        self.doc = None

    def set_doc(self, doc_name):
        self.doc = fitz.open(doc_name)

    def get_page_count(self):
        return len(self.doc)

    def get_doc_list_tab(self):
        page_count = self.get_page_count()
        return [None] * page_count

    def get_doc_list(self, page_num):
        doc_list_tab = self.get_doc_list_tab()
        return doc_list_tab[page_num]

    @staticmethod
    def get_clip(doc_list, zoom):
        """切り取った領域を返す"""
        r = doc_list.rect
        mp = r.tl + (r.br - r.tl) * 0.5  # rect middle point
        mt = r.tl + (r.tr - r.tl) * 0.5  # middle of top edge
        ml = r.tl + (r.bl - r.tl) * 0.5  # middle of left edge
        mr = r.tr + (r.br - r.tr) * 0.5  # middle of right egde
        mb = r.bl + (r.br - r.bl) * 0.5  # middle of bottom edge
        if zoom == 1:  # top-left quadrant
            return fitz.Rect(r.tl, mp)
        elif zoom == 4:  # bot-right quadrant
            return fitz.Rect(mp, r.br)
        elif zoom == 2:  # top-right
            return fitz.Rect(mt, mr)
        elif zoom == 3:  # bot-left
            return fitz.Rect(ml, mb)

    def get_page(self, page_num=0, zoom=0):
        """PDFの指定されたページを返す"""
        doc_list = self.get_doc_list(page_num)
        doc_list_tab = self.get_doc_list_tab()
        if not doc_list:
            doc_list_tab[page_num] = self.doc[page_num].get_displaylist()
            doc_list = doc_list_tab[page_num]
        # zoom指定がない時はフルサイズで返す
        if zoom == 0:
            pix = doc_list.get_pixmap(alpha=False)
        # 指定がある時はクリップした領域を返す
        else:
            clip = self.get_clip(doc_list, zoom)
            mat = fitz.Matrix(2, 2)  # zoom matrix
            pix = doc_list.get_pixmap(alpha=False, matrix=mat, clip=clip)

        return pix.tobytes()


class PdfReader:
    """PDFリーダーGUI"""

    @staticmethod
    def get_zoom(event):
        """ボタンに応じてzoom値を返す"""
        if event == "Clear":
            return 0
        if event == "Top-L":
            return 1
        elif event == "Top-R":
            return 2
        elif event == "Bot-L":
            return 3
        elif event == "Bot-R":
            return 4

    @staticmethod
    def get_next_page(page, total_count):
        """次のページ番号を返す"""
        page += 1
        # トータルページ数に到達していた場合は最初のページ
        if page >= total_count:
            return 0
        else:
            return page

    @staticmethod
    def get_prev_page(page, total_count):
        """前のページ番号を返す"""
        page -= 1
        # マイナスの値になった場合は最後のページ
        if page < 0:
            return total_count - 1
        else:
            return page

    @staticmethod
    def can_goto(page, total_count):
        """gotoできる場合はtrueを返す"""
        if page > total_count:
            return False
        elif page <= 0:
            return False
        else:
            return True

    def event_loop(self):
        """イベントループする"""

        next_page_event = ("Next", "MouseWheel:Down")
        prev_page_event = ("Prev", "MouseWheel:Up")
        zoom_event = ("Clear", "Top-L", "Top-R", "Bot-L", "Bot-R")
        enter_event = chr(13)

        frontend = GuiFrontend()
        window = frontend.window()
        backend = GuiBackend()

        page = 0
        total_page = 0
        doc_name = None

        while True:
            event, values = window.read(timeout=100)
            zoom = 0
            # ページ更新の制御
            is_page_update = False

            if event == sg.WIN_CLOSED:
                break

            if event == 'DOC_NAME':
                doc_name = values['DOC_NAME']
                backend.set_doc(doc_name)
                total_page = backend.get_page_count()
                window['TOTAL_PAGE'].Update(f'/ {total_page}')
                # 既にPDFを見ていて途中で変える場合のため、ページカウントとページ表示をリセット
                window['GOTO'].Update("1")
                page = 0
                is_page_update = True

            # doc_nameが指定されておらず、何らかのイベントが発生
            if event and not doc_name:
                continue

            # 次ページ
            if event in next_page_event:
                page = self.get_next_page(page, total_page)
                window['GOTO'].Update(str(page + 1))
                is_page_update = True

            # 前ページ
            if event in prev_page_event:
                page = self.get_prev_page(page, total_page)
                window['GOTO'].Update(str(page + 1))
                is_page_update = True

            # ズーム関連のイベントが押されたらzoomを取得
            if event in zoom_event:
                zoom = self.get_zoom(event)
                is_page_update = True

            # GOボタンもしくはEnterキーが押されたら指定ページにジャンプ
            if event == 'GO' or event == enter_event:
                # 表示されているページ数を取得
                _page = values['GOTO'].strip()
                # 例えば、既に打たれている数字を消した際に空白が生まれるため
                if not _page:
                    continue
                # 10進数以外が入力された場合を除外
                if not _page.isdecimal():
                    continue
                # 入力値が論理的にGOTOできるかチェック
                if self.can_goto(int(_page), total_page):
                    # 注 Backendのget_dataメソッドでは、リストインデックスからページを取得
                    # そのため、表示されているページ数をマイナス-1しないと一つずれる。
                    page = int(_page) - 1
                    is_page_update = True

            # 表示ページの更新
            if is_page_update or not values['GOTO']:
                data = backend.get_page(page, zoom)
                window['IMAGE'].Update(data=data)


def job():
    gui = PdfReader()
    gui.event_loop()


if __name__ == '__main__':
    job()