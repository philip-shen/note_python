# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QSlider, QWidget
import sys

# ヒアドキュメントで記述
StyleSheet = '''
QWidget {
    background-color: #111111;
    color: #0F0;
} 
QSlider::handle:horizontal {
    background-color: white;
    border: 2px solid #5c5c5c;
    width: 24px;
}
QComboBox {
    border: 1px solid gray;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}
'''

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QGridLayout()
        
        """
        # 方法1
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor('#000'))
        p.setColor(self.foregroundRole(), QColor('#0F0'))
        self.setPalette(p)
        """
        
        """
        # 方法2
        self.setStyleSheet(StyleSheet)
        """
        
        self._set_sliders()
        
        self.setLayout(self.layout)


    def _gen_slider_group(self, context="", init_value=5):
        hbox = QHBoxLayout()
        
        slider = QSlider(Qt.Horizontal, self)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setMinimum(0)
        slider.setMaximum(10)
        slider.setValue(init_value)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1) 

        label = QLabel(str(init_value))
        label.setFont(QFont("Sanserif", 15))
        
        slider.valueChanged.connect(lambda evt: self.valuechange(evt, label))
    
        hbox.addWidget(slider)
        hbox.addWidget(label)
    
        return hbox
    
    def _set_sliders(self):
        self.n_sliders = 10
        for k in range(0, self.n_sliders):
            layout = self._gen_slider_group(context=str(k))
            self.layout.addLayout(layout, k, 0)
            

    def valuechange(self, evt, label):
        label.setText(str(evt))

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())