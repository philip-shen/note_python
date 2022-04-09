"""
date: 2020/12/23
author: @_kurene
"""
import os
import sys
import threading

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QFileDialog
from PyQt5.QtWidgets import QLabel, QSlider, QHBoxLayout
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from audioplayer import AudioPlayer

        
class PyAudioPylerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ap = AudioPlayer()
        self.Init_UI()
        self.show()
        
    def Init_UI(self):
        self.setGeometry(100, 100, 400, 400)
        grid = QGridLayout()
        self.setWindowTitle('PyAudioPlayer')
        
        button_play   = QPushButton("Play")
        button_pause  = QPushButton("Pause")
        button_stop   = QPushButton("Stop")
        button_exit   = QPushButton("Exit")
        button_dialog = QPushButton("Open file")
        self.label = QLabel(self)
        
        grid.addWidget(button_dialog, 0, 0, 1, 3)
        grid.addWidget(button_play,   1, 0)
        grid.addWidget(button_pause,  1, 1)
        grid.addWidget(button_stop,   1, 2)
        grid.addWidget(button_exit,   2, 0, 1, 3)
        grid.addWidget(self.label,    3, 0, 1, 3)
        
        button_dialog.clicked.connect(self.button_openfile)
        button_play.clicked.connect(self.ap.play)
        button_pause.clicked.connect(self.ap.pause)
        button_stop.clicked.connect(self.ap.stop)
        button_exit.clicked.connect(self.button_exit)
        
        hbox = QHBoxLayout()
        
        self.slider_label = QLabel(self)
        self.slider_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.slider_label.setMinimumWidth(160)
        
        slider = QSlider(Qt.Vertical)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setMinimum(-200)
        slider.setMaximum(60)
        slider.setTickInterval(1)
        slider.setValue(0)
        slider.valueChanged.connect(self.change_value)
        self.change_value(0.0)
        

        hbox.addStretch()
        hbox.addWidget(slider)
        hbox.addSpacing(15)
        hbox.addWidget(self.slider_label)
        hbox.addStretch()
        
        grid.addLayout(hbox, 4, 0, 1, 3)
        
        self.setLayout(grid)
        
    def change_value(self, value):
        value_mod = value / 10
        self.slider_label.setText(f"{value_mod:.1f} dB")
        # dB => gain coef.
        self.ap.gain = 10 ** (value_mod/20)
        
    def button_exit(self):
        self.ap.terminate()
        QApplication.quit()
        
    def button_openfile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Audio files (*.wav *.mp3 *.flac)")
        filename = os.path.basename(filepath)
        if os.path.exists(filepath):
            self.label.setText(filename)
            self.label.adjustSize()
            self.ap.set_audiofile(filepath)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PyAudioPylerGUI()
    app.exit(app.exec_())