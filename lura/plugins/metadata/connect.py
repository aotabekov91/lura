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

    def register(self, document):
        self.titleAndAuthor(document)
        document.setDB(self.db)

    def titleAndAuthor(self, document):
        data=self.db.getRow({'field':'did', 'value':document.id()})
        if len(data)==0: 
            self.db.writeRow({'did':document.id()})
            self.db.setField('author', document.embeddedAuthor(), 'did', document.id()) 
            title=document.embeddedTitle()
            if title=='': title=document.filePath().split('/')[-1]
            self.db.setField('title', title, 'did', document.id()) 

    def get(self, did):
        r=self.db.getRow({'field':'did', 'value':did})
        if len(r)>0: return r[0]


class MetadataTable(Table):

    def __init__(self):

        self.fields=[
            'id integer PRIMARY KEY AUTOINCREMENT', 
            'author text',
            'title text',
            'url text',
            'jounal text',
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
            'citationCount int',
            'impactFactor real',
            'createTime datetime',
            'accessTime datetime',
            'foreign key(did) references documents(id)'
            ]
        super().__init__(table='metadata', fields=self.fields)
