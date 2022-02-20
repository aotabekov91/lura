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
        self.db=self.window.plugin.tables.anki

    def write(self, noteId, did, page, position):
        self.db.write(noteId, did, page, position)

class AnkiTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'did int',
            'page int',
            'position text',
            'foreign key(did) references documents(id)'
        ]
        super().__init__(table='anki', fields=self.fields)

    def delete(self, criteria):
        self.removeRow(criteria)

    def write(self, noteId, did, page, position):
        data = {
                'id': noteId,
                'did': did, 
                'page': page,
                'position': position, 
                }

        id = self.get(did, page, position, onlyId=True)

        if id != '':
            data['id'] = id
        self.writeRow(data)

    def get(self, did, page, position, criteria=None, onlyId=False):

        if criteria is None:

            criteria = [
                    {'field': 'did', 'value': did},
                    {'field': 'page', 'value': page},
                    {'field': 'position', 'value': position},
                    ]

        annotations = self.getRow(criteria)

        if len(annotations) > 0:
            if onlyId:
                return annotations[0]['id']
            else:
                return annotations[0]['text']
        else:
            return ''
