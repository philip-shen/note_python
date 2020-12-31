from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui_mainqt import Ui_MainWindow

import logging
import sys

write = None

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])

class MyNewHandler(logging.Handler):

    write = None

    def __init__(self, write_method):
        logging.Handler.__init__(self)
        self.write = write_method

    def emit(self, record):
        self.write(record.message + "\r\n")

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon.ico'))
        self.setupUi(self)
        self.root_folder = ''
        self.ADD_BTN.clicked.connect(self.add_click_handler)
        #self.out_log = MyNewHandler(app_window.write)
        self.out_log = MyNewHandler(QMainWindow.write)
        self.show()
    
    def add_click_handler(self):
        logging.info("ADD MESSAGE")

    def write(self, m):
        try:
            self.edit.moveCursor(PyQt5.QtGui.QTextCursor.End)
        except ImportError:
            self.edit.moveCursor(PySide2.QtGui.QTextCursor.End)

        self.edit.insertPlainText(m)
        if self.out:
            self.out.write(m)


if __name__ == "__main__":

    # app.setStyle("Fusion")
    # app.setWindowIcon(QIcon('icon.ico'))
    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(53, 53, 53))
    # palette.setColor(QPalette.WindowText, Qt.white)
    # palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    # palette.setColor(QPalette.ToolTipBase, Qt.white)
    # palette.setColor(QPalette.ToolTipText, Qt.white)
    # palette.setColor(QPalette.Text, Qt.white)
    # palette.setColor(QPalette.Button, QColor(53, 53, 53))
    # palette.setColor(QPalette.ButtonText, Qt.white)
    # palette.setColor(QPalette.BrightText, Qt.red)
    # palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # palette.setColor(QPalette.HighlightedText, Qt.black)
    # app.setPalette(palette)
    # app.setStyleSheet(
    #     "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
    # )
    app = QApplication(sys.argv)
    app_window = MainWindow(Ui_MainWindow)
    console = MyNewHandler(app_window.write)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    sys.exit(app.exec_())
    window = MainWindow()
    app.exec_()
