from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import Item

class UpDownEdit (Item):

    def __init__(self, *args, **kwargs):

        self.timer=QTimer()
        self.timer.timeout.connect(self.emit_signal)

        super().__init__(*args, **kwargs)

    def setUI(self):

        layout, style_sheet=super().setUI()

        style_sheet += 'QPlainTextEdit{padding: 0px 10px 0px 10px;}'

        self.down = QPlainTextEdit(objectName='downEdit')
        self.down.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.down.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.down.textChanged.connect(self.on_contentChanged)

        layout.addWidget(self.down, 70)

        return layout, style_sheet

    def setTextDown(self, text):

        self.down.show()
        self.down.setPlainText(text)

    def textDown(self): return self.down.toPlainText()

    def getDownSize(self):

        size=self.down.document().size()
        width=int(size.width())
        if size.height()==1.0:
            times=int(width/self.down.size().width())
        else:
            times=size.height()
        if times==0: times=1
        height=int(25*times)
        if height<50: height=50
        size=QSize(width, height)
        return size

    def setFixedWidth(self, width):

        super().setFixedWidth(width)
        self.down.setFixedWidth(width-12) # minus padding
        self.adjustSize()

    def sizeHint(self):

        size=self.up.size()
        s=self.getDownSize()
        size.setHeight(int(size.height()+s.height()+15))
        return size

    def setData(self, data):

        super().setData(data)
        if data:
            if data.get('down', None): self.setTextDown(str(data.get('down')))
            down_color=data.get('down_color', None)

            if down_color: 
                down_style=self.label_style+f'color: black; background-color: {down_color};'+'}'
                self.down.setStyleSheet(down_style)

        self.adjustSize()

    def on_contentChanged(self): 

        self.timer.stop()
        text=self.textDown()
        if text!=str(self.data['down']):
            self.data['down']=self.textDown()
            self.list.adjustSize()
            self.timer.start(500)

    def emit_signal(self):

        self.timer.stop()
        self.list.widgetDataChanged.emit(self)

    def setFocus(self): self.down.setFocus()

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.down.installEventFilter(listener)
