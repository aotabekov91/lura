from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .connect import DatabaseConnector

class Tags(QWidget):

    def __init__(self, parent, settings):
        super().__init__()
        self.window = parent
        self.s_settings = settings
        self.name = 'tags'
        self.globalKeys = {
                'Ctrl+t': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut,)
                }

        self.setup()

    def get(self, uid, kind):
        return self.db.get(uid, kind)

    def getTagged(self, tag):
        return self.db.getTagged(tag)

    def toggle(self):
        
        if self.window.view() is None: return

        if not self.activated:

            self.window.activateStatusBar(self)
            self.lineEdit.setText(self.getTags())
            self.lineEdit.setFocus()
            self.activated=True

        else:

            self.window.deactivateStatusBar(self)
            self.activated=False

    def getTags(self):
        uid=self.window.document().id()
        kind=self.window.document().kind()+'s'
        return self.db.get(uid, kind)

    def addTag(self):
        uid=self.window.document().id()
        if self.window.document().kind()=='document':
            self.db.setTags(uid, 'documents', self.lineEdit.text())
        elif self.window.document().kind()=='root':
            self.db.setTags(uid, 'maps', self.lineEdit.text())
        elif self.window.document().kind()=='annotation':
            self.db.setTags(uid, 'annotations', self.lineEdit.text())
        self.toggle()

    def setup(self):

        self.activated=False

        self.db = DatabaseConnector(self) 

        self.lineEdit=CQLineEdit(self)
        self.label=QLabel('Tags')
        self.lineEdit.returnPressed.connect(self.addTag)
        layout=QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.showTagEdit(cleanUp=True)

class CQLineEdit(QLineEdit):

    def __init__(self, parent):
        super().__init__()
        self.m_parent=parent

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.m_parent.toggle()
        else:
            super().keyPressEvent(event)
