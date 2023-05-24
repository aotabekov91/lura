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
                padding: 5px 0px 0px 5px;
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

        self.setStyleSheet(self.style_sheet)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    # def sizeHint(self):
    #     hint=self.size()
    #     total_height=0
    #     if self.count()>0:
    #         item=self.item(0)
    #         item_height = item.sizeHint().height()
    #         total_height=self.count()*(item_height+2)
    #         total_height+=hint.height()
    #     hint.setHeight(total_height)
    #     return hint

    # def sizeHint(self):
    #     return QSize(200, 800)

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
                padding: 0px 0px 0px 10px;
                background-color: %s; 
                }
            QPlainTextEdit{
                padding: 0px 0px 0px 0px;
                }
                '''%color

        self.setStyleSheet(self.style_sheet)
 
        self.textQVBoxLayout = QVBoxLayout()
        self.textQVBoxLayout.setSpacing(0)
        self.textQVBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel()
        self.title.setWordWrap(True)

        self.content = QPlainTextEdit()
        self.content.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.textQVBoxLayout.addWidget(self.title)
        self.textQVBoxLayout.addWidget(self.content)
        self.textQVBoxLayout.addStretch(1)

        self.setLayout(self.textQVBoxLayout)

        self.setTitle(title)
        if content:
            self.setContent(content)

        self.content.textChanged.connect(self.on_contentChanged)


    def setContent(self, text):
        self.content.setPlainText(text)
        self.content.show()
        self.adjustSize()

    def setTitle(self, text):
        self.title.setText(text)
        self.title.adjustSize()
        self.title.show()

    def resizeEvent(self, event):
        self.adjustSize()

    def adjustSize(self):
        self.title.setFixedWidth(self.size().width()-15)
        self.content.setFixedWidth(self.size().width()-15)
        self.contentHeightChange()

    def contentHeightChange(self):
        self.content.document().adjustSize()
        height = 25 * int(self.content.document().size().height())
        text=self.content.document().toPlainText()
        print(text, height)
        self.content.setFixedHeight(height)
        return height 

    def sizeHint(self):
        self.adjustSize()
        tsize=self.title.size()
        height=tsize.height()+self.contentHeightChange()
        return QSize(tsize.width(), height) 

    def setFixedWidth(self, width):
        super().setFixedWidth(width)
        self.title.setFixedWidth(width)
        self.content.setFixedWidth(width)

    def on_contentChanged(self):
        text=self.content.toPlainText()
        self.contentUpdateOccurred.emit(self.data['id'], text)
