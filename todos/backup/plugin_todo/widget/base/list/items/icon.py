import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import Item

class Icon(Item):

    def installEventFilter(self, listener):

        self.icon.installEventFilter(listener)

    def setUI(self):

        style_sheet = '''

            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                color: transparent;
                background-color: transparent;
                }
            QLabel{
                padding: 0 0 0 0;
                background-color: transparent;
                }
                '''

        self.icon = QLabel()

        w=QWidget()
        layout= QHBoxLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.addStretch()
        layout.addWidget(self.icon, Qt.AlignCenter)
        layout.addStretch()
        w.setLayout(layout)

        layout=QHBoxLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.addStretch()
        layout.addWidget(w, Qt.AlignCenter)
        layout.addStretch()

        return layout, style_sheet

    def setIcon(self, imagePath):

        self.icon.path = imagePath
        if os.path.isfile(imagePath):
            scale=self.icon.size()
            w, h=scale.width(), scale.height()
            self.icon.setPixmap(QPixmap(imagePath).scaled(w, h, Qt.KeepAspectRatio))
            self.icon.show()

    def setData(self, data):

        if data.get('icon', False): self.setIcon(data['icon'])

    def setFixedWidth(self, width):

        self.setFixedSize(self.list.size())
