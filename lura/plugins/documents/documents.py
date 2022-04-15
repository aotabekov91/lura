import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import DocumentsTable

class Documents(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.m_watchFolders=settings['watchFolders']
        self.name = 'documents'
        self.globalKeys={
                'Ctrl+d': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }

        self.setup()

    def setup(self):

        self.activated=False

        self.window.plugin.tables.addTable(DocumentsTable)
        self.db = self.window.plugin.tables.documents

        self.fuzzy = self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.act)

        self.window.documentCreated.connect(self.register)

        self.window.plugin.command.addCommands(
                [('dcd - check documents', 'checkDocuments'),
                    ('dwf - watch folders', 'watchFolders')], self)

    def watchFolders(self):

        # TODO: refactor as a separate process
        for path in self.m_watchFolders:

            qIterator = QDirIterator(
                path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)

            while qIterator.hasNext():
                loc=qIterator.next()
                r=self.window.plugin.tables.get('documents',
                    {'loc':loc})
                if r is None:
                    self.window.buffer.loadDocument(loc)

    def checkDocuments(self):

        # TODO: refactor as a separate process
        allDocs=self.window.plugin.tables.getAll('documents')

        for doc in allDocs:
            loc=doc['loc']
            if not os.path.exists(loc):
                self.window.plugin.tables.remove(
                        'metadata', {'did': doc['id']})
                self.window.plugin.tables.remove(
                        'documents', {'id': doc['id']})

    def setFuzzyData(self, client=None):
        if client is None: client=self

        data=self.db.getAll()
        filePaths=[d['loc'] for d in data]
        locs=[d.split('/')[-1] for d in filePaths]
        names=[]

        for i, d in enumerate(data):
            meta=self.window.plugin.tables.get('metadata', {'did': d['id']})
            if meta is None or meta['title']=='':
                names+=[locs[i]]
            else:
                names+=[meta['title']]

        self.fuzzy.setData(client, filePaths, names)

    def toggle(self):
        self.setFuzzyData()
        self.fuzzy.toggle(self)

    def getFuzzy(self, client):
        self.setFuzzyData(client)
        self.fuzzy.activate(client)

    def act(self, filePath, fuzzyListener):
        if fuzzyListener==self:
            self.window.open(filePath)
        self.toggle()

    def register(self, document):
        filePath=document.filePath()
        data=self.window.plugin.tables.get('documents', {'loc':filePath})

        if data is None:

            self.window.plugin.tables.write('documents', {'loc': filePath})
            data=self.window.plugin.tables.get('documents', {'loc':filePath})

        document.setId(data['id'])
        self.window.documentRegistered.emit(document)
