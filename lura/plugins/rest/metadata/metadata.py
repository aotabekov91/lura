from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .connect import DatabaseConnector

class Metadata(QWidget):

    titleChanged=pyqtSignal(object)

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.db = DatabaseConnector(parent, settings)
        self.location = 'right'
        self.s_settings = settings
        self.globalKeys = {'Ctrl+i': (self.toggle, self.window, Qt.WindowShortcut)}
        self.name = 'metadata'
        self.setup()

    def setup(self):

        self.m_id=None

        self.dropdown = QComboBox(self)
        self.title=MQTextEdit('title', self.window.plugin.tables, self)
        self.tags=MQTextEdit('tags', self.window.plugin.tables, self)
        self.stack = QStackedWidget(self)

        self.m_layout = QVBoxLayout(self)
        self.m_layout.addWidget(self.dropdown)
        self.m_layout.addWidget(self.title)
        self.m_layout.addWidget(QLabel('Tags:'))
        self.m_layout.addWidget(self.tags)
        self.m_layout.addWidget(self.stack)

        self.m_layout.addStretch(1)

        self.m_layout.setContentsMargins(0, 0, 0, 0)

        for i in ['Book', 'Paper', 'Website']:
            self.dropdown.addItem(i)

        self.dropdown.currentTextChanged.connect(self.on_dropdown_changed)

        self.book = ['author', 'publisher', 'year', 'edition', 'address', 'bibkey']
        self.paper = ['author', 'journal', 'year', 'volume', 'number', 'pages',
                'bibkey']
        self.website = ['author', 'url', 'bibkey']

        self.createWidgets()

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.mapItemChanged.connect(self.on_mapItemChanged)
        self.window.titleChanged.connect(self.title.on_titleChanged)
        self.window.documentTagged.connect(self.on_documentTagged)

        self.titleChanged.connect(self.window.titleChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def createWidgets(self):

        for k in ['book', 'paper', 'website']:

            setattr(self, f'{k}Tab', QWidget(self.stack))
            tab = getattr(self, f'{k}Tab')
            tab.layout = QFormLayout(tab)
            tab.layout.setContentsMargins(0, 0, 0, 0)

            fields={}
            for field in getattr(self, f'{k}'):
                qline = MQLineEdit(field, self.window.plugin.tables, self)
                qline.setParent(tab)
                tab.layout.addRow(field.title(), qline)
                fields[field]=qline
            setattr(self, f'{k}TabIndex', self.stack.addWidget(tab))
            setattr(self, f'{k}Fields', fields)

    def on_mapItemChanged(self, item):
        if not self.isVisible(): return
        if item is None or item.kind()!='document': return

        self.m_id=item.id()
        self.setKind(item.id())

    def on_viewChanged(self, view):
        if not self.isVisible(): return
        if view is None: return
        self.m_id = view.document().id()
        self.setKind(self.m_id)

    def on_documentTagged(self, m_id, kind, tagList, sender):
        if sender==self.tags: return
        if not self.isVisible(): return
        if self.m_id!=m_id: return
        self.tags.textChanged.disconnect()
        self.tags.setPlainText('; '.join(tagList))
        self.tags.connect()

    def on_dropdown_changed(self):
        if self.m_id is None: return
        kind = self.dropdown.currentText().lower()
        self.window.plugin.tables.update(
                'metadata', {'did':self.m_id}, {'kind':kind})
        self.setKind(self.m_id)
        self.stack.setCurrentIndex(self.index)

    def toggle(self, forceShow=False):

        # if self.window.document() is None: return
        if not self.isVisible(): 

            self.window.activateTabWidget(self)
            if self.m_id is None: return
            self.setKind(self.m_id)
            self.stack.setCurrentIndex(self.index)
            self.setFocus()

        else:
            self.window.deactivateTabWidget(self)

    def setKind(self, did):
        self.kind = self.window.plugin.tables.get('metadata', {'did':did}, 'kind')
        if self.kind==None: self.kind='paper'
        self.dropdown.setCurrentText(self.kind.title())

        self.title.textChanged.disconnect()
        self.title.setPlainText(
                self.window.plugin.tables.get(
                    'metadata', {'did':did}, 'title'))
        self.title.connect()

        tags=self.window.plugin.tags.get(did, 'document')
        self.tags.textChanged.disconnect()
        self.tags.setPlainText('; '.join(tags))
        self.tags.connect()

        if self.kind in [None, '']: self.kind = 'book'

        self.index = getattr(self, f'{self.kind}TabIndex')
        fields = getattr(self, f'{self.kind}Fields')

        for field, qline in fields.items():
            qline.disconnect()
            qline.setText(
                    str(self.window.plugin.tables.get(
                'metadata', {'did':did}, field)))
            qline.connect()

    def register(self, document):
        self.db.register(document)

class MQTextEdit(QPlainTextEdit):
    def __init__(self, field, data, meta):
        super().__init__()
        self.meta=meta
        self.field = field
        self.m_data=data
        self.textChanged.connect(self.on_textChanged)
        self.setFixedHeight(60)

    def connect(self):
        self.textChanged.connect(self.on_textChanged)

    def on_titleChanged(self, sender):
        if self==sender: return

        title=self.meta.window.plugin.tables.get(
                    'metadata', {'did':self.meta.m_id}, 'title')
        self.setPlainText(title)
        self.moveCursor(QTextCursor.End)

    def on_textChanged(self):
        if self.field=='title':
            self.m_data.update(
                    'metadata', 
                    {'did':self.meta.m_id}, 
                    {self.field:self.toPlainText().lower().title()})
            self.meta.titleChanged.emit(self)
        elif self.field=='tags':
            tagList=[a.strip() for a in self.toPlainText().split(';')]
            self.meta.window.plugin.tags.set(
                    self.meta.m_id, 'document', tagList)
            self.meta.window.documentTagged.emit(
                    self.meta.m_id, 'document', tagList, self)

class MQLineEdit(QLineEdit):
    def __init__(self, field, data, meta):
        super().__init__()
        self.meta=meta
        self.field = field
        self.m_data=data
        self.textChanged.connect(self.on_textChanged)

    def connect(self):
        self.textChanged.connect(self.on_textChanged)

    def on_textChanged(self, text):
        if text=='': return
        self.m_data.update(
                'metadata', 
                {'did':self.meta.m_id}, 
                {self.field:text.lower().title()})
