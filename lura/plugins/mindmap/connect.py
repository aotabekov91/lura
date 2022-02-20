from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring

from .table import MapsTable

class DatabaseConnector:

    def __init__(self, parent, window):
        self.m_parent=parent
        self.window=window
        self.setup()

    def setup(self):
        self.window.plugin.tables.addTable(MapsTable)
        self.db=self.window.plugin.tables.maps
        self.window.mapCreated.connect(self.register)

    def title(self, mapp):
        return self.db.getRow({'field':'id','value':mapp.id()})[0]['title']

    def setTitle(self, mapp, title):
        self.db.updateRow(
                {'field':'id', 'value':mapp.id()}, {'title':title})

    def setContent(self, mapp, content):
        self.db.updateRow({'field':'id', 'value':mapp.id()}, {'content':content})

    def getAll(self):
        return self.db.getAll()

    def get(self, mid):
        return self.db.getRow({'field':'id', 'value':mid})[0]

    def register(self, mapp):
        mapp.setDB(self)
        if mapp.id() is not None: return

        data={'title':'Mindmap', 'content':''}
        self.db.writeRow(data)
        mapp.setId(self.db.getAll()[-1]['id'])

    def delete(self, mid):
        criteria={'field': 'id', 'value':mid}
        self.db.removeRow(criteria)

    def write(self, data):
        self.db.writeRow(data)

    def setId(self, mapp):
        self.write({'title':'Mindmap', 'content': mapp.tree()})
        mapp.setId(self.getAll()[-1]['id'])

