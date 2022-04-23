from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .connect import DatabaseConnector

from lura.core.miscel import MapTree

from lura.core.miscel import Item
from lura.core.miscel import ItemModel

from .display import MapView

class MindMap(MapTree):

    def __init__(self, parent, settings):
        super().__init__(parent, parent)
        self.window=parent
        self.display=MapView(self, parent)
        self.location='left'
        self.name='mindmap'
        self.globalKeys = {
                'Ctrl+m': (
                    self.showMindmaps,
                    self.window,
                    Qt.WindowShortcut),
                'Ctrl+Shift+m': (
                    self.display.toggle,
                    self.window,
                    Qt.WindowShortcut),
                }
        self.setup()

    def setup(self):

        self.db=DatabaseConnector(self, self.window)
        self.window.setTabLocation(self, self.location, self.name)

    def showMindmaps(self):
        mindmaps=self.window.plugin.tables.get('maps')

        model=ItemModel()
        model.itemChanged.connect(self.on_itemChanged)

        for m in mindmaps:
            item=Item('map', m['id'], self.window, m['title'])
            model.appendRow(item)

        self.setModel(model)
        self.window.activateTabWidget(self)
        self.setFocus()

    def open(self):
        item=self.currentItem()
        if item is None: return

        model=ItemModel(item.id(), self.window)

        self.db.register(model)
        self.display.openModel(model)

    def addNode(self):
        model=ItemModel(None, self.window)
        self.db.register(model)

        self.display.openModel(model)

    def delete(self):
        item=self.currentItem()
        if item is None: return

        self.window.plugin.tables.remove('maps', {'id': item.id()})
        self.showMindmaps()

    def on_itemChanged(self, item):
        self.window.plugin.tables.update(
                'maps', {'id': item.id()}, {'title':item.text()})

    def close(self):
        self.window.deactivateTabWidget(self)
