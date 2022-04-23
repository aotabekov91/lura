import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import DocumentsTable

from lura.core.miscel import *

class Documents(MapTree):

    def __init__(self, parent, settings):
        super().__init__(parent, parent)
        self.window=parent
        self.m_watchFolders=settings['watchFolders']
        self.name = 'documents'
        self.location='bottom'
        self.globalKeys={
                'Ctrl+d': (
                    self.showDocuments,
                    self.window,
                    Qt.WindowShortcut)
                }

        self.setup()

    def setup(self):

        self.window.plugin.tables.addTable(DocumentsTable)
        self.db = self.window.plugin.tables.documents

        self.window.documentCreated.connect(self.register)

        self.window.plugin.command.addCommands(
                [('dcd - check documents', 'checkDocuments'),
                    ('dwf - watch folders', 'watchFolders')], self)

        self.window.setTabLocation(self, self.location, self.name)

    def showDocuments(self):
        documents=self.window.plugin.tables.get('documents')

        model=ItemModel()
        model.itemChanged.connect(self.on_itemChanged)

        for d in documents:
            item=Item('document', d['id'], self.window)
            model.appendRow(item)

        self.setModel(model)
        self.window.activateTabWidget(self)
        self.setFocus()

    def on_itemChanged(self, item):
        self.window.plugin.tables.update(
                'metadata', {'did':item.id()}, {'title':item.text().title()})

    def open(self):
        item=self.currentItem()
        if item is None: return

        filePath=self.window.plugin.tables.get(
                'documents', {'id':item.id()}, 'loc')
        print(filePath)
        self.window.open(filePath)
        self.setFocus()

    def watchFolders(self):

        # TODO: refactor as a separate process
        for path in self.m_watchFolders:

            qIterator = QDirIterator(
                path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)

            while qIterator.hasNext():
                loc=qIterator.next()
                r=self.window.plugin.tables.get('documents', {'loc':loc})
                if r is None:
                    self.window.buffer.loadDocument(loc)

    def checkDocuments(self):

        # TODO: refactor as a separate process
        allDocs=self.window.plugin.tables.get('documents')

        for doc in allDocs:
            loc=doc['loc']
            if not os.path.exists(loc):
                self.window.plugin.tables.remove(
                        'metadata', {'did': doc['id']})
                self.window.plugin.tables.remove(
                        'documents', {'id': doc['id']})

    def register(self, document):
        filePath=document.filePath()
        data=self.window.plugin.tables.get('documents', {'loc':filePath})

        if data is None:

            self.window.plugin.tables.write('documents', {'loc': filePath})
            data=self.window.plugin.tables.get('documents', {'loc':filePath})

        document.setId(data['id'])
        self.window.documentRegistered.emit(document)

    def close(self):
        self.window.deactivateTabWidget(self)
