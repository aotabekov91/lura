import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import DocumentsTable

class Documents(QObject):

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.window=parent
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

    def setFuzzyData(self, client=None):
        if client is None: client=self

        data=self.db.getAll()
        filePaths=[d['loc'] for d in data]
        locs=[d.split('/')[-1] for d in filePaths]
        names=[]

        for i, d in enumerate(data):
            meta=self.window.plugin.metadata.get(d['id'])
            if meta is None:
                names+=[locs[i]]
            else:
                if meta['title']=='':
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

    def getByLoc(self, filePath):
        return self.db.getRow({'field':'loc', 'value':filePath})

    def getData(self, did):
        return self.db.getRow({'field':'id', 'value':did})[0]

    def get(self, did):
        documentData=self.db.getRow({'field':'id', 'value':did})[0]
        return self.window.buffer.loadDocument(documentData['loc'])

    def register(self, document):
        data=self.getByLoc(document.filePath())
        if len(data)==0: 
            if not document.shouldRegister(): return

            data= self.db.getRow({'field': 'loc', 'value': document.filePath()})
            if len(data) == 0: self.db.writeRow({'loc': document.filePath()})
            data= self.db.getRow({'field': 'loc', 'value': document.filePath()})

        document.setId(data[0]['id'])
        self.window.documentRegistered.emit(document)

    def getAll(self):
        return self.db.getAll()
