#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .table import MetadataTable

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
        document.setDB(self)

    # def content(self, document):
    #     if not document.registered(): return
    #     return self.db.getRow({'field':'did', 'value':document.id()})[0]['content']

    # def setContent(self, document, content):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'content':content})

    # def title(self, document):
    #     if type(document)==int:
    #         return self.db.getRow({'field':'did', 'value':document})[0]['title']
    #     else:
    #         if not document.registered(): return
    #         return self.db.getRow({'field':'did', 'value':document.id()})[0]['title']

    # def setTitle(self, document, title):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'title':title})

    # def url(self, document):
    #     if not document.registered(): return
    #     return self.db.getRow({'field':'did', 'value':document.id()})[0]['url']

    # def setUrl(self, document, url):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'url':url})

    # def kind(self, document):
    #     if not document.registered(): return
    #     return self.db.getRow({'field':'did', 'value':document.id()})[0]['kind']

    # def setKind(self, document, kind):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'kind':kind})

    # def accessTime(self, document):
    #     if not document.registered(): return
    #     return self.db.getRow({'field':'did', 'value':document.id()})[0]['accessTime']

    # def setAccessTime(self, document, accessTime):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'accessTime':accessTime})

    # def year(self, document):
    #     if not document.registered(): return
    #     return self.db.getRow({'field':'did', 'value':document.id()})[0]['year']

    # def setYear(self, document, year):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'year':year})

    # def author(self, document):
    #     if not document.registered(): return
    #     return self.db.getRow({'field':'did', 'value':document.id()})[0]['author']

    # def setAuthor(self, document, author):
    #     if not document.registered(): return
    #     self.db.updateRow({'field':'did', 'value':document.id()}, {'author':author})

    # def titleAndAuthor(self, document):
    #     data=self.db.getRow({'field':'did', 'value':document.id()})
    #     if len(data)==0: 
    #         self.db.writeRow({'did':document.id()})
    #         author=document.embeddedAuthor()
    #         title=document.embeddedTitle()
    #         if title=='': title=document.filePath().split('/')[-1]
    #         self.setAuthor(document, author) 
    #         self.setTitle(document, title)

    def get(self, did):
        r=self.db.getRow({'field':'did', 'value':did})
        if len(r)>0: return r[0]
