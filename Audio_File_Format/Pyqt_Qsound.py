"""
date: 2020/12/20
author: @_kurene
"""
import os
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QFileDialog
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtMultimedia import QSound

        
class PyAudioPylerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.qsound = None
        self.init_ui()
        self.show()
        
    def init_ui(self):
        self.setGeometry(100, 100, 250, 250)
        grid = QGridLayout()
        self.setWindowTitle('PyQt AudioPlayer with QSound')
        
        #grid.setSpacing(10)
        button_play   = QPushButton("Play")
        button_stop   = QPushButton("Stop")
        button_exit   = QPushButton("Exit")
        button_dialog = QPushButton("Open audio-file")
        self.label = QLabel(self)
        
        grid.addWidget(button_dialog, 0, 0, 1, 2)
        grid.addWidget(button_play,   1, 0)
        grid.addWidget(button_stop,   1, 1)
        grid.addWidget(button_exit,   2, 0, 1, 2)
        grid.addWidget(self.label,    3, 0, 1, 2)
        
        button_dialog.clicked.connect(self.button_openfile)
        button_play.clicked.connect(self.button_play)
        button_stop.clicked.connect(self.button_stop)
        button_exit.clicked.connect(self.button_exit)
        
        self.setLayout(grid)
        
    def button_exit(self):
        QApplication.quit()
        
    def button_play(self):
        if self.qsound is not None: 
            self.qsound.play()
     
    def button_stop(self):
        if self.qsound is not None: 
            self.qsound.stop()
        
    def button_openfile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Audio files (*.wav)")
        filepath = os.path.abspath(filepath)
        
        self.qsound = QSound(filepath)
        
        self.filename = os.path.basename(filepath)
        self.label.setText(self.filename)
        self.label.adjustSize()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PyAudioPylerGUI()
    app.exit(app.exec_())