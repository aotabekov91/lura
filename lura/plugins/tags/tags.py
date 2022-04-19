from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.view.docviewer import DocumentView

from .connect import DatabaseConnector

class Tags(QObject):

    def __init__(self, parent, settings):
        super().__init__()
        self.window = parent
        self.s_settings = settings
        self.name = 'tags'
        self.db = DatabaseConnector(self) 

        self.globalKeys = {
            'Ctrl+t': (
                self.tag,
                self.window,
                Qt.WindowShortcut)
        }


    def tag(self):
        if type(self.window.view())==DocumentView:
            m_id=self.window.view().document().id()
            tags=self.get(m_id, 'document')
        else:
            document=self.window.view().tree()
            item=document.currentItem()
            if item is None: return
            m_id=item.id()
            kind=item.kind()
            tags=self.get(m_id, kind)

        text='; '.join(tags)
        self.window.plugin.command.activateCustom(
                self._tag, 'Tag: ', text=text)

    def _tag(self, text):
        if type(self.window.view())==DocumentView:
            document=self.window.view().document()
            m_id=document.id()
            kind='document'
        else:
            document=self.window.view().tree()
            item=document.currentItem()
            if item is None: return
            m_id=item.id()
            kind=item.kind()

        tags=[a.strip() for a in text.split(';')]
        self.set(m_id, kind, tags)

        self.window.documentTagged.emit(m_id, kind, tags, self)
        self.window.view().setFocus()

    def get(self, m_id, kind='document'):
        return self.db.get(m_id, kind)

    def set(self, m_id, kind, tagList):
        self.db.set(m_id, kind, tagList)
