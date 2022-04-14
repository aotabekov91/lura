from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class BaseTreeWidget(QWidget):

    sizeChanged=pyqtSignal()
    pushButtonClicked=pyqtSignal(object)

    def __init__(self, data):
        super().__init__()
        self.m_data=data
        self.setup()

    def setup(self):

        self.m_colored=False
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        layout=QVBoxLayout(self)

        title=self.m_data.getField('title')
        if title is None: title=''
        self.m_titleEdit=CQTextEdit(title.lower().title())
        self.m_titleEdit.textChanged.connect(self.on_titleChanged)
        self.m_titleEdit.sizeChanged.connect(self.sizeChanged)

        self.m_metaEdit=QWidget()
        self.m_metaEdit.m_layout=QFormLayout(self.m_metaEdit)

        self.m_metaEdit.m_layout.setVerticalSpacing(0)
        self.m_metaEdit.m_layout.setHorizontalSpacing(10)
        self.m_metaEdit.m_layout.setContentsMargins(0, 2, 0, 2)

        layout.addWidget(self.m_titleEdit)
        layout.addWidget(self.m_metaEdit)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 2)
        layout.addStretch(1)

        self.addSubFields()

    def addSubFields(self):
        self.addTagsField()
        self.addIDField()

        self.m_metaEdit.hide()

        self.hideEdit(self.m_tagEdit)
        self.hideEdit(self.m_idEdit)
        if hasattr(self, 'm_contentEdit'): self.hideEdit(self.m_contentEdit)
        if hasattr(self, 'm_authorEdit'): self.hideEdit(self.m_authorEdit)

    def hideEdit(self, edit):
        edit.hide()
        if hasattr(edit, 'm_label'): edit.m_label.hide()

    def showEdit(self, edit):
        edit.show()
        if hasattr(edit, 'm_label'): edit.m_label.show()

    def addIDField(self):
        self.m_idEdit=QLabel('{}/{}'.format(self.m_data.getField('kind'), self.m_data.id()))
        self.m_idEdit.m_label=QLabel('ID')
        self.m_metaEdit.m_layout.addRow(self.m_idEdit.m_label, self.m_idEdit)

    def addContentField(self):
        self.m_contentEdit=CQTextEdit(self.m_data.getField('content'))
        self.m_contentEdit.textChanged.connect(self.on_contentChanged)
        self.m_contentEdit.sizeChanged.connect(self.sizeChanged)
        self.m_contentEdit.m_label=QLabel('Content')
        self.m_metaEdit.m_layout.addRow(self.m_contentEdit.m_label, self.m_contentEdit)

    def addQuoteField(self):
        self.m_quoteEdit=CQTextEdit(self.m_data.getField('quote'))
        self.m_quoteEdit.textChanged.connect(self.on_quoteChanged)
        self.m_quoteEdit.sizeChanged.connect(self.sizeChanged)
        self.m_quoteEdit.m_label=QLabel('Quote')
        self.m_metaEdit.m_layout.addRow(self.m_quoteEdit.m_label, self.m_quoteEdit)

    def addAuthorField(self):
        self.m_authorEdit=CQTextEdit(self.m_data.getField('author'))
        self.m_authorEdit.textChanged.connect(self.on_authorChanged)
        self.m_authorEdit.sizeChanged.connect(self.sizeChanged)
        self.m_authorEdit.m_label=QLabel('Authors')
        self.m_metaEdit.m_layout.addRow(self.m_authorEdit.m_label, self.m_authorEdit)

    def addTagsField(self):
        self.m_tagEdit=CQTextEdit(self.m_data.tags())
        self.m_tagEdit.textChanged.connect(self.on_tagChanged)
        self.m_tagEdit.sizeChanged.connect(self.sizeChanged)
        self.m_tagEdit.m_label=QLabel('Tags')
        self.m_metaEdit.m_layout.addRow(self.m_tagEdit.m_label, self.m_tagEdit)

    def on_quoteChanged(self):
        pass

    def on_authorChanged(self):
        self.m_data.setAuthor(self.m_authorEdit.toPlainText())

    def on_contentChanged(self):
        self.m_data.setContent(self.m_contentEdit.toPlainText())

    def on_titleChanged(self):
        self.m_data.setTitle(self.m_titleEdit.toPlainText())

    def on_tagChanged(self):
        self.m_data.setTags(self.m_tagEdit.toPlainText())

    def height(self):
        height=2.
        height+=self.m_titleEdit.height()
        if self.m_metaEdit.isVisible(): height+=2
        if self.m_tagEdit.isVisible(): height+=self.m_tagEdit.height()+2
        if self.m_idEdit.isVisible(): height+=self.m_idEdit.height()+2
        if hasattr(self, 'm_contentEdit'):
            if self.m_contentEdit.isVisible(): height+=self.m_contentEdit.height()+2
        if hasattr(self, 'm_authorEdit'):
            if self.m_authorEdit.isVisible(): height+=self.m_authorEdit.height()+2
        if hasattr(self, 'm_quoteEdit'):
            if self.m_quoteEdit.isVisible(): height+=self.m_quoteEdit.height()+2
        return height

    def change(self, kind):
        if not hasattr(self, f'm_{kind}Edit'): return
        edit=getattr(self, f'm_{kind}Edit')
        if edit is not None:
            if kind!='title': self.m_metaEdit.show()
            if not edit.isVisible(): self. toggle(kind)
            edit.moveCursor(QTextCursor.End)
            self.setFocus()
            edit.setFocus()

    def toggle(self, kind):
        if kind == 'color':
            self.toggleColor()
        else:
            if not hasattr(self, f'm_{kind}Edit'): return
            edit=getattr(self, f'm_{kind}Edit')

            if edit.isVisible():
                self.m_metaEdit.hide()
                self.hideEdit(edit)
            else:
                self.m_metaEdit.show()
                self.showEdit(edit)
            self.sizeChanged.emit()

    def toggleColor(self):
        if not self.m_colored:
            color=self.m_data.getField('color')
            if color is not None:
                color=color.name()
                self.m_titleEdit.setStyleSheet(f'background-color:{color}')
                self.m_colored=True
        else:
            self.m_titleEdit.setStyleSheet(f'background-color:{white}')
            self.m_colored=False

class CQTextEdit(QPlainTextEdit):

    sizeChanged=pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.onTextChanged)
        self.onTextChanged()
        self.setFixedHeight(25)

    def onTextChanged(self):
        self.show()
        newHeight=self.document().size().toSize().height()*25
        if newHeight!=self.height():
            self.setFixedHeight(newHeight)
            self.sizeChanged.emit()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.parent().setFocus()
            event.accept()
        else:
            super().keyPressEvent(event)
