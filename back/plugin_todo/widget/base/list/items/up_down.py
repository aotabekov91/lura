from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import Item

class UpDown(Item):

    def setUI(self):

        layout, style_sheet = super().setUI()

        self.down = QLabel(objectName='downElement')
        self.down.setWordWrap(True)

        layout.removeWidget(self.up)

        layout.addWidget(self.up, 50)
        layout.addWidget(self.down, 50)

        layout.addStretch()

        self.up.hide()
        self.down.hide()

        return layout, style_sheet 

    def setTextDown(self, text):

        self.down.setText(str(text))
        self.down.show()
        self.down.adjustSize()

    def textDown(self): return self.down.text()

    def setData(self, data):

        super().setData(data)

        if data:
            if data.get('down', None):
                self.setTextDown(str(data.get('down')))
                color=data.get('down_color', None)
                if color: 
                    self.setStyleSheet(
                            self.style_sheet + ' '.join(
                        ['QLabel#downElement{',
                         f'background-color: {color};',
                         'color: black;}',
                         ]))

        self.adjustSize()

    def setFixedWidth(self, width):

        self.down.setFixedWidth(width-12) # minus padding
        super().setFixedWidth(width)
        self.adjustSize()

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.down.installEventFilter(listener)

    def sizeHint(self):

        size=super().sizeHint()
        size_up=self.up.size()
        size.setWidth(size_up.width())
        return size

