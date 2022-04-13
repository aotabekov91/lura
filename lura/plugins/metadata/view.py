#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .connect import DatabaseConnector


class Metadata(QWidget):

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

        self.activated = False
        self.m_id=None

        self.dropdown = QComboBox(self)
        self.title=MQTextEdit('title', self.window.plugin.tables, self)
        self.stack = QStackedWidget(self)

        self.m_layout = QVBoxLayout(self)
        self.m_layout.addWidget(self.dropdown)
        self.m_layout.addWidget(self.title)
        self.m_layout.addWidget(self.stack)

        self.m_layout.addStretch(1)

        self.m_layout.setContentsMargins(0, 0, 0, 0)

        for i in ['Book', 'Paper', 'Website']:
            self.dropdown.addItem(i)

        self.dropdown.currentTextChanged.connect(self.on_dropdown_changed)

        self.book = ['author', 'publisher', 'year', 'edition', 'address']
        self.paper = ['author', 'journal', 'year', 'volume', 'number', 'pages']
        self.website = ['author', 'url']

        self.createWidgets()

        self.window.viewChanged.connect(self.on_viewChanged)
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

    def on_viewChanged(self):
        if not self.activated: return
        self.activated = not self.activated
        self.toggle()

    def on_dropdown_changed(self):
        if self.m_id is None: return
        kind = self.dropdown.currentText().lower()
        self.window.plugin.tables.update(
                'metadata', {'did':self.m_id}, {'kind':kind})
        self.setKind(self.m_id)
        self.stack.setCurrentIndex(self.index)

    def toggle(self, forceShow=False):

        if self.window.document() is None:
            return

        if not self.activated or forceShow:

            self.m_id = self.window.document().id()
            self.setKind(self.m_id)
            self.stack.setCurrentIndex(self.index)
            self.setFocus()
            self.window.activateTabWidget(self)
            self.activated = True

        else:
            self.window.deactivateTabWidget(self)
            self.activated = False

    def setKind(self, did):
        self.kind = self.window.plugin.tables.get('metadata', {'did':did}, 'kind')
        self.dropdown.setCurrentText(self.kind.title())
        self.title.setPlainText(
                self.window.plugin.tables.get(
                    'metadata', {'did':did}, 'title'))
        if self.kind in [None, '']: self.kind = 'book'

        self.index = getattr(self, f'{self.kind}TabIndex')
        fields = getattr(self, f'{self.kind}Fields')

        for field, qline in fields.items():
            qline.setText(
                    str(self.window.plugin.tables.get(
                'metadata', {'did':did}, field)))

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

    def on_textChanged(self):
        self.m_data.update(
                'metadata', 
                {'did':self.meta.m_id}, 
                {self.field:self.toPlainText().lower().title()})

class MQLineEdit(QLineEdit):
    def __init__(self, field, data, meta):
        super().__init__()
        self.meta=meta
        self.field = field
        self.m_data=data
        self.textChanged.connect(self.on_textChanged)

    def on_textChanged(self, text):
        self.m_data.update(
                'metadata', 
                {'did':self.meta.m_id}, 
                {self.field:text.lower().title()})
