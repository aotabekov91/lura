import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from ..base import BrowserWidget
from ..base import InputLabelWidget

class InputBrowser(QWidget):

    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    returnPressed=pyqtSignal()
    hideWanted=pyqtSignal()

    def __init__ (self, input_class=InputLabelWidget, title=None):

        super(InputBrowser, self).__init__()

        self.waiting=False
        self.setInputWidget(input_class=input_class)

        self.setUI()

        if title: self.input.setLabel(title)

    def setUI(self):

        self.style_sheet='''
            QWidget{
                font-size: 16px;
                color: cyan;
                border-width: 0px;
                border-radius: 0px;
                }
            QWidget#browserContainer{
                border-color: red;
                border-width: 2px;
                border-radius: 10px;
                border-style: outset;
                color: white;
                background-color: transparent;
                }
                '''

        self.input.setMaximumHeight(40)
        self.browser = BrowserWidget()

        self.browser.setStyleSheet(self.style_sheet)

        w=QWidget(objectName='browserContainer')
        layout=QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(7,7,7,7)
        layout.addWidget(self.browser)
        w.setLayout(layout)
        w.setStyleSheet(self.style_sheet)

        layout=QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(self.input)
        layout.addWidget(w)

        self.setLayout(layout)
        self.setStyleSheet(self.style_sheet)

        self.input.hideWanted.connect(self.hideWanted)
        self.browser.hideWanted.connect(self.hideWanted)

    def setInputWidget(self, input_class):

        self.input=input_class()

        self.input.textChanged.connect(self.inputTextChanged)

        self.input.returnPressed.connect(self.returnPressed)
        self.input.returnPressed.connect(self.inputReturnPressed)

    def installEventFilter(self, listener):

        self.input.installEventFilter(listener)
        self.browser.installEventFilter(listener)

    def show(self):

        super().show()
        self.input.setFocus()

    def hide(self):
        self.hideWanted.emit()
        super().hide()

    def setFocus(self):

        self.input.setFocus()

    def clear(self):

        self.input.clear()
