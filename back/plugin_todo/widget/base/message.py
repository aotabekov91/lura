import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MessageWidget(QWidget):

    hideWanted=pyqtSignal()

    def __init__ (self):
        super(MessageWidget, self).__init__(objectName='mainWidget')

        self.pause=False

        self.style_sheet='''
            QWidget{
                font-size: 20px;
                color: white;
                border-color: transparent;
                background-color: back;
                border-width: 2px;
                border-style: outset;
                border-radius: 10px;
                border-color: red;
                background-color: #101010;
                padding: 10px 10px 10px 10px;
                }
            QLabel{
                color: white;
                background-color: green;
                border-width: 0px
                border-color: transparent;
                }
                '''

        self.setStyleSheet(self.style_sheet)

        self.title=QLabel('title')
        self.title.setWordWrap(True)
        self.information=QLabel()
        self.information.setWordWrap(True)
        self.detail=QLabel()
        self.detail.setWordWrap(True)

        # self.title.hide()
        # self.information.hide()
        # self.detail.hide()

        layout=QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        layout.addWidget(self.title, 10)
        layout.addWidget(self.information, 50)
        layout.addWidget(self.detail, 40)
        layout.addStretch(1)

        self.setLayout(layout)
        self.adjustSize()

    def installEventFilter(self, listener):
        super().installEventFilter(listener)
        self.title.installEventFilter(listener)
        self.detail.installEventFilter(listener)
        self.information.installEventFilter(listener)

    def setTitle(self, text):
        text=text.strip().title()
        self.title.setText(text)
        self.title.adjustSize()
        self.title.show()
        self.adjustSize()

    def setDetail(self, text):
        text=text.strip()
        self.detail.setText(text)
        self.detail.adjustSize()
        self.detail.show()
        self.adjustSize()

    def setInformation(self, text):
        text=text.strip()
        self.information.setText(text)
        self.information.adjustSize()
        self.information.show()
        self.adjustSize()

    def setTimer(self, timeout):
        QTimer.singleShot(timeout, self.hide)

    def setPause(self):
        self.pause=True
