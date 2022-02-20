from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .connect import DatabaseConnector

from lura.core.widgets import Menu

class MindMap(Menu):

    def __init__(self, parent, settings):
        mapping={getattr(self, f):v for f, v in settings['shortcuts'].items()}
        super().__init__(parent, mapping)
        self.window=parent
        self.name='mindmap'
        self.location='bottom'
        self.globalKeys={
                'Ctrl+Shift+d': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.activated=False

        self.db=DatabaseConnector(self, self.window)

        self.fuzzy=self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.on_fuzzySelected)
        self.setFuzzyData()

        self.window.setTabLocation(self, self.location, self.name)

    def setFuzzyData(self):
        maps = self.db.getAll()
        names = [m['title'] for m in maps]
        self.fuzzy.setData(self, maps, names)

    def hide(self):
        if self.isVisible():
            super().hide()
            self.window.deactivateTabWidget(self)
       
    def toggle(self):
        if not self.activated:
            self.window.activateTabWidget(self)
            self.setFocus()
            self.activated=True
        else:
            self.window.deactivateTabWidget(self)
            self.activated=False

    def openMap(self):
        self.mode='open'
        self.fuzzy.activate(self)

    def createMap(self):
        self.toggle()
        self.window.open('map:new')

    def deleteMap(self):
        self.mode='delete'
        self.fuzzy.activate(self)

    def on_fuzzySelected(self, selected, client):
        if client!=self: return
        self.fuzzy.deactivate(self)
        self.toggle()
        if self.mode=='open':
            filePath='map:{}'.format(selected['id'])
            self.window.open(filePath)
        elif self.mode=='delete':
            self.db.delete(selected['id'])
            self.setFuzzyData()
            self.toggle()
            self.fuzzy.activate(self)
