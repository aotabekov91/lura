#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.plugins.tables import Table 

class DatabaseConnector(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.s_settings=settings
        self.setup()

    def setup(self):

        self.window.plugin.tables.addTable(MetadataTable)
        self.db=self.window.plugin.tables.metadata
        self.window.documentRegistered.connect(self.register)

        self.window.plugin.command.addCommands(
                [('iad - meta add title', 'addTitle')], self)

    def addTitle(self):
        allDocuments=self.window.plugin.tables.getAll('documents')
        for f in allDocuments:
            meta=self.window.plugin.tables.get('metadata', {'did':f['id']})
            if meta is None: self.window.buffer.loadDocument(f['loc'])

    def register(self, document):
        self.titleAndAuthor(document)

    def titleAndAuthor(self, document):
        data=self.db.getRow({'field':'did', 'value':document.id()})
        if len(data)==0: 
            self.db.writeRow({'did':document.id()})
            self.db.setField('author', document.author(), 'did', document.id()) 
            title=document.title().lower().title()
            filePath=self.window.plugin.tables.get(
                    'documents', {'id':document.id()}, 'loc')
            if title=='': title=filePath.split('/')[-1]
            self.db.setField('title', title, 'did', document.id()) 


class MetadataTable(Table):

    def __init__(self):

        self.fields=[
            'id integer PRIMARY KEY AUTOINCREMENT', 
            'author text',
            'title text',
            'url text',
            'journal text',
            'year int',
            'volume int',
            'number int',
            'edition int', 
            'pages text',
            'publisher text',
            'address text',
            'bibkey text',
            'kind text',
            'did int unique',
            'hash text',
            'type text',
            'createTime datetime',
            'accessTime datetime',
            'foreign key(did) references documents(id)'
            ]
        super().__init__(table='metadata', fields=self.fields)
