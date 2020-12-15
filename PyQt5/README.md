
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

[Anaconda附属のPyQt5とQtDesigerにてGUI作成 Nov 03, 2018](https://qiita.com/zack0828/items/d71c7123a518bb6cfb56)

[PyQt5とpython3によるGUIプログラミング［１］Jun 12, 2016](https://qiita.com/kenasman/items/70a3ef914b0e7e55a123)  
[PyQt5とpython3によるGUIプログラミング［２］Jun 14, 2016](https://qiita.com/kenasman/items/73d01df973a25ae704e4)  
[PyQt5とpython3によるGUIプログラミング［３］Jul 09, 2016](https://qiita.com/kenasman/items/794d2874d56d0dc37aea)  
[PyQt5とpython3によるGUIプログラミング［４］Jul 09, 2016](https://qiita.com/kenasman/items/3119efb6ee1c53dbd877)  
[PyQt5とpython3によるGUIプログラミング［５］Sep 12, 2016](https://qiita.com/kenasman/items/4da65dd4dd4192f30c21)  
[PyQt5とpython3によるGUIプログラミング［６］Sep 24, 2016](https://qiita.com/kenasman/items/765457d440b923f4e555)  
[PyQt5とpython3によるGUIプログラミング［7-1］Nov 21, 2016](https://qiita.com/kenasman/items/87c12f3a8b63f5948153)  
[PyQt5とpython3によるGUIプログラミング［7-2］（編集中）Feb 23, 2017](https://qiita.com/kenasman/items/b3d5b7c8cd442c3c4429)  
[PyQt5とpython3によるGUIプログラミング［８］（編集中）Feb 18, 2017](https://qiita.com/kenasman/items/fb3f1260c355585a5dce)  

[PyQt5とpython3によるGUIプログラミング：実践編[0] Feb 04, 2019](https://qiita.com/kenasman/items/b9ca3beb25ecf87bfb06)  

# Display logs in PyQt  
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