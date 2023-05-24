from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CustomListWidget(QListWidget):

    def __init__(self, parent=None):
        super(CustomListWidget, self).__init__(parent)

        self.style_sheet = '''
            QListWidget{
                border-width: 0px;
                color: transparent;
                border-color: transparent; 
                background-color: transparent; 
                }
            QListWidget::item{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                border-style: outset;
                padding: 5px 5px 5px 5px;
                color: transparent;
                border-color: transparent;
                background-color: #101010;
                }
            QListWidget::item:selected {
                border-width: 2px;
                border-color: red;
                }
                '''

        self.setWordWrap(True)
        self.setSpacing(1)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.adjustSize()
        self.setStyleSheet(self.style_sheet)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def sizeHint(self):
        hint=self.size()
        total_height=0
        if self.count()>0:
            item=self.item(0)
            item_height = item.sizeHint().height()
            total_height=self.count()*(item_height+2)
            if total_height > 500:
                total_height=(500//item_height)*item_height
            total_height+=hint.height()
        hint.setHeight(total_height)
        return hint

    def keyPressEvent(self, event):
        self.parent().keyPressEvent(event)

class CustomListItem (QWidget):

    contentUpdateOccurred=pyqtSignal(int, str)
    def __init__(self, data, parent=None):
        super(CustomListItem, self).__init__(parent)
        self.data=data

        title = self.data.get('title', '')
        content = self.data.get('content', '')
        color = self.data.get('color', 'transparent')

        self.style_sheet = '''
            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                background-color: transparent;
                }
            QLabel{
                color: grey;
                font-size: 16px;
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                padding: 2px 10px 2px 10px;
                background-color: %s; 
                }
                '''%color

        self.setStyleSheet(self.style_sheet)
 
        self.textQVBoxLayout = QVBoxLayout()
        self.textQVBoxLayout.setSpacing(0)
        self.textQVBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel()
        self.title.setWordWrap(True)

        self.content = QTextEdit()

        self.textQVBoxLayout.addWidget(self.title)
        self.textQVBoxLayout.addWidget(self.content)
        self.textQVBoxLayout.addStretch(1)

        self.setLayout(self.textQVBoxLayout)

        self.setTitle(title)
        if content:
            self.setContent(content)
            self.content.setFixedHeight(70)
        else:
            self.content.hide()

        self.content.textChanged.connect(self.on_contentChanged)

    def setContent(self, text):
        self.content.setText(text)
        self.content.show()

    def setTitle(self, text):
        self.title.setText(text)
        self.title.adjustSize()
        self.title.show()

    def adjustSize(self):
        self.title.adjustSize()
        self.content.adjustSize()

    def on_contentChanged(self):
        text=self.content.toPlainText()
        self.contentUpdateOccurred.emit(self.data['id'], text)
