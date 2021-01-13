
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [PyQt5とpython3](#pyqt5とpython3)
      * [PyQt5インストール（Windows編）](#pyqt5インストールwindows編)
      * [Button, RadioButton](#button-radiobutton)
      * [ComboBox](#combobox)
      * [File Open Dialogue](#file-open-dialogue)
      * [QTableWidget](#qtablewidget)
      * [tablewidgetのセルの色を変えてみる](#tablewidgetのセルの色を変えてみる)
      * [デジタル時計を表示](#デジタル時計を表示)
      * [Windowのstyleを変えてみる](#windowのstyleを変えてみる)
      * [standardIcon](#standardicon)
      * [QGraphicsSceneに楕円と矩形を置いてマウスで移動可能にする](#qgraphicssceneに楕円と矩形を置いてマウスで移動可能にする)
   * [Qt Designer](#qt-designer)
      * [起動方法・画面説明](#起動方法画面説明)
      * [モード](#モード)
   * [Display logs in PyQt](#display-logs-in-pyqt)
   * [Detect resizing in Widget-window](#detect-resizing-in-widget-window)
   * [PyQt5 GUI](#pyqt5-gui)
      * [リスト選択のGUIを作る](#リスト選択のguiを作る)
   * [PyQt5 pyinstaller](#pyqt5-pyinstaller)
      * [2 対策](#2-対策)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of PyQt5  


# PyQt5とpython3  
[PyQt5とpython3によるGUIプログラミング Nov 06, 2016](https://qiita.com/kenasman/items/471b9930c0345562cbbf)  
```
ページが増えてきたので、目次を作ります。
PyQt5とpython3によるGUIプログラミング［０］
MacとWindowsのインストール方法です。

PyQt5とpython3によるGUIプログラミング［１］
PyQt５のサンプルコードです。

PyQt5とpython3によるGUIプログラミング［２］
PyQt５のサンプルコードその２です。

PyQt5とpython3によるGUIプログラミング［３］
MVCのマニュアルの日本語訳です。

PyQt5とpython3によるGUIプログラミング［４］
MVCのサンプルコードです。

PyQt5とpython3によるGUIプログラミング［５］
PyQt5_Examplesのコードを紹介していきます。

PyQt5とpython3によるGUIプログラミング［６］
Qt DesignerでのGUI作成サンプルです。

PyQt5とpython3によるGUIプログラミング［7-1］
Paint Systemの翻訳です。
```

[PyQt5とpython3によるGUIプログラミング［０］Jun 12, 2016](https://qiita.com/kenasman/items/55505654823e9d040e6e)  
## PyQt5インストール（Windows編）  
```
■Qtのオープンソースをインストール  

■pythonインストール

■sipのインストール

■PyQt5のインストール

■起動確認
```


[Anaconda附属のPyQt5とQtDesigerにてGUI作成 Nov 03, 2018](https://qiita.com/zack0828/items/d71c7123a518bb6cfb56)

[PyQt5とpython3によるGUIプログラミング［１］Jun 12, 2016](https://qiita.com/kenasman/items/70a3ef914b0e7e55a123)  

## Button, RadioButton  
<img src=""  width="300" height="400">

## ComboBox  
<img src=""  width="300" height="400">

## File Open Dialogue  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F124460%2F3c7e41a8-9659-cf35-2d82-04448b307efa.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=1156b31a9ef5ede3c5f8aee54ddbb2ba"  width="300" height="100">

[PyQt5 tutorial August 14, 2020](http://zetcode.com/gui/pyqt5/)
[ janbodnar /PyQt5-Tutorial-Examples](https://github.com/janbodnar/PyQt5-Tutorial-Examples)  

## QTableWidget  
<img src=""  width="300" height="400">

## tablewidgetのセルの色を変えてみる  
<img src=""  width="300" height="400">  

## デジタル時計を表示  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F124460%2Fbd4671e2-6032-f76b-9448-30a27346d7c7.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=1e43e2197c89c09882709dc7dfc53b60"  width="300" height="100">

```
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TestTimer(QWidget):

    def __init__(self, parent=None):

        super(TestTimer, self).__init__(parent)
        self.setWindowTitle('Digital Clock')
        timer = QTimer(self)

        timer.timeout.connect(self.updtTime)
        self.testTimeDisplay = QLCDNumber(self)
        self.testTimeDisplay.setSegmentStyle(QLCDNumber.Filled)
        self.testTimeDisplay.setDigitCount(8)
        self.testTimeDisplay.resize(500, 150)
        self.updtTime()
        timer.start(1000)

    def updtTime(self):

        currentTime = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.testTimeDisplay.display(currentTime)

if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    myWindow = TestTimer()
    myWindow.show()
    myApp.exec_()
    sys.exit()
```
## Windowのstyleを変えてみる  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F124460%2F43c9c5e0-c5e4-ab06-775b-12b13289029a.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=06d8d1d8df3622d7c6d0a629a8e16809"  width="300" height="400">  

## standardIcon  
[List of Qt Icons September 23, 2015](https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/)  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F124460%2F07ee7d07-b4d1-9b7d-81a5-6387af88e6d7.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=4b49776ba9c303180ad7e5512121654c"  width="300" height="400">  

## QGraphicsSceneに楕円と矩形を置いてマウスで移動可能にする  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F124460%2F5cbef573-dd68-a1fc-2a5f-805e61dd0dc1.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=ed06bff892fc424a6240273de2323ff0"  width="300" height="400">  

[PyQt5とpython3によるGUIプログラミング［２］Jun 14, 2016](https://qiita.com/kenasman/items/73d01df973a25ae704e4)  



[PyQt5とpython3によるGUIプログラミング［３］Jul 09, 2016](https://qiita.com/kenasman/items/794d2874d56d0dc37aea)  
[PyQt5とpython3によるGUIプログラミング［４］Jul 09, 2016](https://qiita.com/kenasman/items/3119efb6ee1c53dbd877)  
[PyQt5とpython3によるGUIプログラミング［５］Sep 12, 2016](https://qiita.com/kenasman/items/4da65dd4dd4192f30c21)  


# Qt Designer  
[PyQt5とpython3によるGUIプログラミング［６］Sep 24, 2016](https://qiita.com/kenasman/items/765457d440b923f4e555)  
```
Qt Designerで画面を作り、uiファイルをpythonのソースに変換する方法を示していきます。
```

```
※なぜ、これをもっと初めに紹介しなかったかというと、実はこのツールは中級から上級者が対象のためでした。
ツール類は基本を理解していることが前提で作られているようなので、初心者がいきなりこのツールを使って、
思うものを作ろうとすると大体は挫折してしまうようです。
```

```
Qt Designer 自体の使い方は、Qt Designer使い方入門Qt Designer使い方入門 がわかりやすい。
```


```
ユーザインタフェースを設計し.uiファイルに保存した後、使用する前に、それをコードに変換しなければなりません。
これはpyuic5コマンドラインプログラムを使用して行います。
.uiファイルのあるディレクトリで、以下を実行します。
```

## pyuic5
```
pyuic5 -o ui_test_designer.py test_designer.ui
```

```
ここで注意が必要なのは上記のコマンドで作成したpythonのコードを直接編集してはいけないということです。
なぜなら次にpyuic5コマンドを実行すると上書きされるため、追加したコードは消えてしまいます。
```

[Qt Designer使い方入門 Feb-2014](http://vivi.dyndns.org/tech/Qt/QtDesigner.html)

## 起動方法・画面説明  
<img src="http://vivi.dyndns.org/tech/Qt/QtDesigner.png"  width="600" height="400">

## モード  
```
QtDesigner には以下の４つの動作モードがあります。

   1. ウィジェットの編集 F3
   2. シグナル/スロットの編集 F4
   3. buddy の編集
   4. タブ順序の編集
```

## QT Designer for UI  
[用QT Designer 制作Maya工具UI 2018-04-04](https://zhuanlan.zhihu.com/p/35278775)  
 
<img src="https://pic1.zhimg.com/80/v2-208e6b492440ff950151a0d5891b3e80_720w.jpg"  width="300" height="400">
```
其中最重要的是 objectName, 可以对所选widget重新命名，这个名称将会在代码中调用，
建立widget和function 的关联(创建slot,后面会详细讲)。

将建立好的文件储存到任意的文件夹，这里我命名为 ui_test.ui

接下来就是在maya的python脚本编辑器里调用这个 .ui 文件。
```

```
调用 .ui 文件有两种方式，一种是先将 .ui 文件convert成 python 脚本文件, 然后调用；
也可以直接导入 .ui文件，这里我倾向使用后者。
至于第一种方法，网上已有教程，我就不讲了。
```

```
首先说明一下一些定义：

在QT里面，对widget的每一次“操作”称为signal, 不同的widget有不同signal，
signal也不是唯一的，不同的signal可以让不同“操作”有不同的影响。

具体的signal可以在文档中搜索到，比如：
```



<img src=""  width="300" height="400">


## Qt Designer in Virtual Environment   
[PyQt5 基本教學 (1) 安裝 PyQt5，印出 Hello World! 2019-08-26](https://clay-atlas.com/blog/2019/08/26/python-chinese-pyqt5-tutorial-install/)
```
首先我們必須安裝以下兩個套件：

pip3 install PyQt5
pip3 install pyqt5-tools

其中 PyQt5 便是我們要安裝的套件名稱；pyqt5-tools 裡面則是包含了圖形界面開發程式 QtDesigner.exe。

這裡建議不要裝在 PyCharm 專案的虛擬環境裡，而是直接裝在系統上。  
```
> 虛擬環境

```
C:\Users\Philip.Shen\Envs\3quest\Lib\site-packages\qt5_applications\Qt\bin\designer.exe
```


[PyQt5とpython3によるGUIプログラミング［7-1］Nov 21, 2016](https://qiita.com/kenasman/items/87c12f3a8b63f5948153)  
[PyQt5とpython3によるGUIプログラミング［7-2］（編集中）Feb 23, 2017](https://qiita.com/kenasman/items/b3d5b7c8cd442c3c4429)  
[PyQt5とpython3によるGUIプログラミング［８］（編集中）Feb 18, 2017](https://qiita.com/kenasman/items/fb3f1260c355585a5dce)  

[PyQt5とpython3によるGUIプログラミング：実践編[0] Feb 04, 2019](https://qiita.com/kenasman/items/b9ca3beb25ecf87bfb06)  

# Display logs in PyQt  
[A Qt GUI for logging - Plumber Jack 15 November 2019](http://plumberjack.blogspot.com/2019/11/a-qt-gui-for-logging.html)  
```
A question that comes up from time to time is about how to log to a GUI application. 
The Qt framework is a popular cross-platform UI framework with Python bindings using PySide2 or PyQt5 libraries.

The following example shows how to log to a Qt GUI. This introduces a simple QtHandler class which takes a callable, which should be a slot in the main thread that does GUI updates. 
A worker thread is also created to show how you can log to the GUI from both the UI itself (via a button for manual logging) as well as a worker thread doing work in the background (here, just logging messages at random levels with random short delays in between).

The worker thread is implemented using Qt’s QThread class rather than the threading module, 
as there are circumstances where one has to use QThread, which offers better integration with other Qt components.

The code should work with recent releases of either PySide2 or PyQt5. 
You should be able to adapt the approach to earlier versions of Qt. 
Please refer to the comments in the code snippet for more detailed information.
```

[同步logging訊息到 QT GUI上 Jul 22, 2018](https://medium.com/@webeasyplay.cr/%E5%90%8C%E6%AD%A5logging%E8%A8%8A%E6%81%AF%E5%88%B0-qt-gui%E4%B8%8A-49af3f9788a1)
```
再來我們有三件事情要做
1. 建立ADD_BTN的click事件來做測試
2. 自定義一個logging.HANDLER
3. 把Mywidge的write 方法在MyNewHandler傳入，讓emit調用
```


[Best way to display logs in pyqt? Feb 22](https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt?noredirect=1&lq=1)
```
import sys
from PyQt5 import QtWidgets
import logging

# Uncomment below for terminal log messages
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MyDialog(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self._button = QtWidgets.QPushButton(self)
        self._button.setText('Test Me')

        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        layout.addWidget(self._button)
        self.setLayout(layout)

        # Connect signal to slot
        self._button.clicked.connect(self.test)

    def test(self):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')

app = QtWidgets.QApplication(sys.argv)
dlg = MyDialog()
dlg.show()
dlg.raise_()
sys.exit(app.exec_())
```

[How to Redirect Logger Output into PyQt Text Widget ](https://stackoverflow.com/questions/24469662/how-to-redirect-logger-output-into-pyqt-text-widget)
```
import sys
from PyQt4 import QtCore, QtGui
import logging

class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        record = self.format(record)
        if record: XStream.stdout().write('%s\n'%record)
        # originally: XStream.stdout().write("{}\n".format(record))


logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)
    def flush( self ):
        pass
    def fileno( self ):
        return -1
    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))
    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout
    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr

class MyDialog(QtGui.QDialog):
    def __init__( self, parent = None ):
        super(MyDialog, self).__init__(parent)

        self._console = QtGui.QTextBrowser(self)
        self._button  = QtGui.QPushButton(self)
        self._button.setText('Test Me')

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._console)
        layout.addWidget(self._button)
        self.setLayout(layout)

        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        self._button.clicked.connect(self.test)

    def test( self ):
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warning message')
        logger.error('error message')
        print 'Old school hand made print message'

if ( __name__ == '__main__' ):
    app = None
    if ( not QtGui.QApplication.instance() ):
        app = QtGui.QApplication([])
    dlg = MyDialog()
    dlg.show()
    if ( app ):
        app.exec_()
```

[Redirecting Output in PyQt Jul 13](https://stackoverflow.com/questions/11465971/redirecting-output-in-pyqt)

[同步logging訊息到QT GUI上 Jul 22, 2018](https://medium.com/@webeasyplay.cr/%E5%90%8C%E6%AD%A5logging%E8%A8%8A%E6%81%AF%E5%88%B0-qt-gui%E4%B8%8A-49af3f9788a1)
[ webeasyplay /logging_sync_qt](https://github.com/webeasyplay/logging_sync_qt)

[Python Log Viewer](https://pythonhosted.org/logview/)  


# Detect resizing in Widget-window  
[Detect resizing in Widget-window resized signal Mar 30 '17](https://stackoverflow.com/questions/43126721/detect-resizing-in-widget-window-resized-signal)  

[Basic-Pyqt5](https://github.com/webeasyplay/Basic-Pyqt5) 


# Lineedit, TextEdit, Plaintextedit  
[The difference between Lineedit, TextEdit, Plaintextedit three controls in QT 2014-12-03](https://topic.alibabacloud.com/a/the-difference-between-lineedit-textedit-plaintextedit-three-controls-in-qt_8_8_31580469.html)  
```
Qlineedit is a single-line text input, generally used for user names, passwords and other small text interaction places.
Qtextedit is used for multiple lines of text, or it can display HTML-formatted text.
Qplaintextedit is much like Qtextedit, but it is used in places where it needs to be processed with text, and Qtextedit is used for display, so to speak, qplaintextedit for plain The text processing ability is stronger than TextEdit.

The difference between Lineedit, TextEdit, Plaintextedit three controls in QT
```


# PyQt5 GUI      
[PythonのPyQtによるクロスプラットフォームGUIアプリ作成入門](https://myenigma.hatenablog.com/entry/2016/01/24/113413)

## リスト選択のGUIを作る  
[リスト選択のGUIを作る](https://myenigma.hatenablog.com/entry/2016/01/24/113413#%E3%83%AA%E3%82%B9%E3%83%88%E9%81%B8%E6%8A%9E%E3%81%AEGUI%E3%82%92%E4%BD%9C%E3%82%8B)  



# PyQt5 pyinstaller    
[pyinstaller ビルド時の”Cannot find existing PyQt5 plugin directories” Jan 27, 2019](https://qiita.com/tatsuruM/items/cd657f25022c93d0284f)  
```
Cannot find existing PyQt5 plugin directories
```

## 2 対策
```
PyQt5が見つからない場合の対策も上記のサイトに紹介されているのですが、うまくいきません。

PyQt5をconda installでインストールしようとしましたが、以下のようにはじかれてしまいます。

    UnsatisfiableError: The following specifications were found to be in conflict:
    - pyqt5 -> python=3.5
    - python=3.6
    Use "conda info " to see the dependencies for each package.

python3.6に対応してないということでしょうか？
先ほどのエラーをよくみると、以下のパスをチェックしろと書いてあります。

    Exception:
    Cannot find existing PyQt5 plugin directories
    Paths checked: C:/Miniconda3/conda-bld/qt_1535195524645/_h_env/Library/plugins

それで指示されている「/Miniconda3/.../plugins」フォルダを作成し、

    Anacondaインストールフォルダ\envs\仮想環境名\Library\plugins\

にあるplatformsフォルダをフォルダごとコピー

    pyinstaller --onefile hogehoge.py

再ビルドで無事にexeファイルが作成できました。
```

# Troubleshooting



# Reference


* []()  
![alt tag]()  
<img src=""  width="300" height="400">

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3


