from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.plugins.tables import Table

class DatabaseConnector:

    def __init__(self, parent, window):
        self.m_parent=parent
        self.window=window
        self.setup()

    def setup(self):
        self.window.plugin.tables.addTable(NotesTable)
        self.db=self.window.plugin.tables.notes

    def register(self, note):
        data={'title':note.title(), 'loc':note.filePath()}
        self.window.plugin.tables.write(data)
        nid=self.window.plugin.tables.get(
                'notes', {'loc':note.filePath()}, 'id')
        note.setId(nid)


class NotesTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'did integer',
            'title text',
            'loc text',
            'foreign key(did) references documents(id)',

        ]
        super().__init__(table='notes', fields=self.fields)
