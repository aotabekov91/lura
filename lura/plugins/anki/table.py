from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.plugins.tables import Table

class AnkiNote(object):

    def __init__(self, parent):
        self.window=parent
        self.setup()

    def setup(self):
        self.window.plugin.tables.addTable(AnkiTable)

class AnkiTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'nid int',
            'did int',
            'page int',
            'position text',
            'foreign key(did) references documents(id)'
        ]
        super().__init__(table='anki', fields=self.fields)
