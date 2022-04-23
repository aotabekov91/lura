from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .connect import DatabaseConnector
from lura.core.miscel import ItemModel

class MindMap(QObject):

    def __init__(self, parent, settings):
        super().__init__()
        self.window=parent
        self.name='mindmap'
        self.setup()

    def setup(self):

        self.activated=False
        self.db=DatabaseConnector(self, self.window)

        self.fuzzy=self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.on_fuzzySelected)

        commandList=[('mo - open a map', 'openMap'),
                    ('mc - create a map', 'createMap'),
                    ('md - delete a map', 'deleteMap')]

        self.window.plugin.command.addCommands(commandList, self)

    def setFuzzyData(self):
        maps = self.window.plugin.tables.get('maps')
        names = [m['title'] for m in maps]
        self.fuzzy.setData(self, maps, names)

    def openMap(self):
        self.mode='open'
        self.setFuzzyData()
        self.fuzzy.activate(self)

    def createMap(self):
        model=ItemModel(None, self.window)
        self.db.register(model)
        self.window.plugin.mapviewer.open(model)

    def deleteMap(self):
        self.mode='delete'
        self.setFuzzyData()
        self.fuzzy.activate(self)

    def on_fuzzySelected(self, selected, client):
        if client!=self: return
        self.fuzzy.deactivate(self)
        if self.mode=='open':
            model=ItemModel(selected['id'], self.window)
            self.db.register(model)
            self.window.plugin.itemviewer.open(model)
        elif self.mode=='delete':
            self.window.plugin.tables.remove(
                    'maps', {'id': selected['id']})
            self.setFuzzyData()
            self.fuzzy.activate(self)
