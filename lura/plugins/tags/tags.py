from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.view.docviewer import DocumentView

from .display import TagView
from .connect import DatabaseConnector

class Tags(QObject):

    def __init__(self, parent, settings):
        super().__init__()
        self.window = parent
        self.name='tags'
        self.s_settings = settings
        self.display=TagView(self, self.window)
        self.db = DatabaseConnector(self)

        self.globalKeys = {
            'Ctrl+t': (
                self.tag,
                self.window,
                Qt.WindowShortcut),
            'Ctrl+Shift+t': (
                self.display.toggle,
                self.window,
                Qt.WindowShortcut)
        }
        self.setup()

    def setup(self):
        self.m_item=None
        self.window.mapItemChanged.connect(self.on_mapItemChanged)

    def on_mapItemChanged(self, item):
        self.m_item=item

    def open(self, model):
        self.display.openModel(model)
        self.window.activateTabWidget(self.display)
        self.display.setFocus()

    def tag(self):
        if type(self.window.view())==DocumentView:
            m_id=self.window.view().document().id()
            tags=self.get(m_id, 'document')
        else:
            if self.m_item is None: return
            if self.m_item.kind()!='document': return
            m_id=self.m_item.id()
            kind=self.m_item.kind()
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
            if self.m_item is None: return
            if self.m_item.kind()!='document': return
            m_id=self.m_item.id()
            kind=self.m_item.kind()

        tags=[a.strip() for a in text.split(';')]
        self.set(m_id, kind, tags)

        self.window.documentTagged.emit(m_id, kind, tags, self)

    def get(self, m_id, kind='document'):
        return self.db.get(m_id, kind)

    def set(self, m_id, kind, tagList):
        self.db.set(m_id, kind, tagList)

    def untag(self, kind, m_id, tag):
        self.db.untag(kind, m_id, tag)
