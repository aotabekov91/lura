from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.plugins.tables import Table

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
