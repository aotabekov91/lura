from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.widgets.tree.widgets import NoteTreeWidget

class Note(QObject):

    wasModified=pyqtSignal(object)
    
    def __init__(self, m_id=None, title=None, content=None):
        super().__init__()
        self.m_id=m_id
        self.m_title=title
        self.m_content=content

    def kind(self):
        return 'note'

    def widget(self):
        return NoteTreeWidget(self)

    def id(self):
        return self.m_id

    def title(self):
        return self.m_db.title(self)

    def content(self):
        return self.m_db.content(self)

    def db(self):
        return self.m_db

    def setDB(self, db):
        self.m_db=db

    def tags(self):
        return self.tagDB.elementTags(self)

    def setTags(self, tags):
        self.tagDB.setElementTags(self, tags)

    def setTagDB(self, db):
        self.tagDB=db

    def setId(self, m_id):
        self.m_id=m_id

    def setTitle(self, title):
        self.m_db.setTitle(self, title)
        self.wasModified.emit(self)

    def setContent(self, content):
        self.m_db.setContent(self, content)
        self.wasModified.emit(self)

    def color(self):
        return

    def setColor(self, color):
        self.m_color=color
