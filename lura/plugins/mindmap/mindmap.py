from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .connect import DatabaseConnector

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
        self.setFuzzyData()

        commandList=[('mo - open a map', 'openMap'),
                    ('mc - create a map', 'createMap'),
                    ('md - delete a map', 'deleteMap')]

        self.window.plugin.command.addCommands(commandList, self)

    def setFuzzyData(self):
        maps = self.db.getAll()
        names = [m['title'] for m in maps]
        self.fuzzy.setData(self, maps, names)

    def openMap(self):
        self.mode='open'
        self.fuzzy.activate(self)

    def createMap(self):
        self.window.open('map:new')

    def deleteMap(self):
        self.mode='delete'
        self.fuzzy.activate(self)

    def on_fuzzySelected(self, selected, client):
        if client!=self: return
        self.fuzzy.deactivate(self)
        if self.mode=='open':
            filePath='map:{}'.format(selected['id'])
            self.window.open(filePath)
        elif self.mode=='delete':
            self.db.delete(selected['id'])
            self.setFuzzyData()
            self.fuzzy.activate(self)
