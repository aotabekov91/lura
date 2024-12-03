from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import Item

class LeftRightEdit (Item):

    def __init__(self, *args, **kwargs):

        self.timer=QTimer()
        self.timer.timeout.connect(self.emit_signal)

        super().__init__(*args, **kwargs)

    def setUI(self):

        style_sheet = '''
            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                background-color: transparent;
                }
            QLabel{
                padding: 0px 10px 0px 10px;
                }
            QPlainTextEdit{
                padding: 0px 10px 0px 10px;
                }
                '''

        left_right_layout = QHBoxLayout()
        left_right_layout.setSpacing(0)
        left_right_layout.setContentsMargins(0, 10, 0, 10)

        self.left = QLabel(objectName='leftLabel')
        self.left.setWordWrap(True)

        self.right = QPlainTextEdit(objectName='rightEdit')
        self.right.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right.textChanged.connect(self.on_contentChanged)

        left_right_layout.addWidget(self.left)
        left_right_layout.addWidget(self.right)
        left_right_layout.addStretch(1)

        return left_right_layout, style_sheet

    def setTextRight(self, text):

        self.right.setPlainText(text)
        self.adjustSize()

    def setTextLeft(self, text):

        self.left.setText(text)
        self.left.adjustSize()

    def textLeft(self):

        return self.left.text()

    def textRight(self): return self.right.toPlainText()

    def adjustSize(self): 

        super().adjustSize()
        self.left.adjustSize()
        self.right.adjustSize()

    def getRightSize(self):

        size=self.right.document().size()
        width=int(size.width())
        if size.height()==1.0:
            times=int(width/self.right.size().width())
        else:
            times=size.height()
        if times==0: times=1
        height=int(50*times)
        if height<50: height=50
        size=QSize(width, height)
        return size

    def setFixedWidth(self, width):

        super().setFixedWidth(width)

        self.adjustSize()

        substract=self.left.size().width()+30
        self.right.setFixedWidth(width-substract)

        self.setFixedHeight(self.getRightSize().height()+15)
        self.right.setFixedHeight(self.getRightSize().height())
        self.adjustSize()

    def setData(self, data):

        super().setData(data)
        if data:
            if data.get('left', None):
                self.setTextLeft(str(data.get('left')))
                color=data.get('left_color', None)
                if color: 
                    self.left.setStyleSheet(f'background-color: {color}; color: black;')
            if data.get('right', None):
                self.setTextRight(str(data.get('right')))
                color=data.get('left_color', None)
                if color: 
                    self.left.setStyleSheet(f'background-color: {color}; color: black;')
            self.adjustSize()

    def setFocus(self): 

        self.right.setFocus()
        cursor=self.right.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.right.setTextCursor(cursor)

    def installEventFilter(self, listener):

        self.left.installEventFilter(listener)
        self.right.installEventFilter(listener)

    def on_contentChanged(self): 

        self.timer.stop()
        text=self.textRight()
        if text!=str(self.data['right']):
            self.data['right']=text
            self.list.adjustSize()
            self.timer.start(500)

    def emit_signal(self):

        self.timer.stop()
        self.list.widgetDataChanged.emit(self)

