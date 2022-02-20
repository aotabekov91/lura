from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .note import Note
from .table import NotesTable

class DatabaseConnector:

    def __init__(self, parent, window):
        self.m_parent=parent
        self.window=window
        self.setup()

    def setup(self):
        self.window.plugin.tables.addTable(NotesTable)
        self.db=self.window.plugin.tables.notes

    def register(self, note):
        note.setDB(self)
        if note.id() is not None: return
        data={'title':'', 'content':''}
        self.db.writeRow(data)
        note.setId(self.db.getAll()[-1]['id'])
        self.window.noteRegistered.emit(note)

    def get(self, nid):
        data=self.db.getRow({'field':'id', 'value':nid})
        if len(data)==0: return
        note=Note(nid, data[0]['title'], data[0]['content'])
        note.setDB(self)
        self.window.noteRegistered.emit(note)
        return note

    def delete(self, nid):
        self.db.removeRow({'field':'id', 'value':nid})

    def getByDid(self, did):
        data=self.db.getRow({'field':'did', 'value':did})
        notes=[]
        for n in data:
            notes+=[self.get(n['id'])]
        return notes

    def getAll(self):
        return self.db.getAll()

    def title(self, note):
        data=self.db.getRow({'field':'id', 'value':note.id()})
        if len(data)>0: return data[0]['title']

    def setTitle(self, note, title):
        self.db.updateRow({'field':'id', 'value':note.id()}, {'title':title})

    def content(self, note):
        data=self.db.getRow({'field':'id', 'value':note.id()})
        if len(data)>0: return data[0]['content']

    def setContent(self, note, content):
        self.db.updateRow({'field':'id', 'value':note.id()}, {'content':content})
