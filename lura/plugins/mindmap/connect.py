from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring

from lura.plugins.tables import Table

class DatabaseConnector:

    def __init__(self, parent, window):
        self.m_parent=parent
        self.window=window
        self.setup()

    def setup(self):
        self.window.plugin.tables.addTable(MapsTable)
        self.window.mapCreated.connect(self.register)

    def register(self, mapp):
        mapp.setDB(self)
        if mapp.id() is not None: return

        allMaps=self.window.plugin.tables.get('maps')
        if allMaps is None or len(allMaps)==0:
            newId=0
        else:
            newId=max([a['id'] for a in allMaps])+1
        data={'title':'Mindmap', 'content':'', 'id':newId}
        self.window.plugin.tables.write('maps', 
                data)
        mapp.setId(newId)


class MapsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'title text',
            'content text',
        ]
        super().__init__(table='maps', fields=self.fields)
