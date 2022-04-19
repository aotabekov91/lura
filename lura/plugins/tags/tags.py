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
        if type(self.window.view())!=DocumentView: return
        did=self.window.view().document().id()
        tags=self.window.plugin.tags.get(did, 'document')
        text='; '.join(tags)
        self.window.plugin.command.activateCustom(
                self._tag, 'Tag: ', self._tag, text=text)

    def _tag(self, text):
        document=self.window.view().document()
        tags=[a.strip() for a in text.split(';')]
        self.set(document.id(), 'document', tags)

    def get(self, m_id, kind='document'):
        return self.db.get(m_id, kind)

    def set(self, m_id, kind, tagList):
        self.db.set(m_id, kind, tagList)
        self.window.documentTagged.emit(m_id, kind, tagList)
