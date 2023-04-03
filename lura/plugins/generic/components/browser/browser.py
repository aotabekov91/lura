import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils.widgets import *

class Documents(MapTree):

    def __init__(self, app):
        super(Documents, self).__init__(app)
        self.app=app
        self.name = 'documents'
        self.location='top'
        self.globalKeys={
                'Ctrl+d': (
                    self.showDocuments,
                    self.app,
                    Qt.WindowShortcut)
                }

        self.app.window.setTabLocation(self, self.location, self.name)

    def showDocuments(self):
        documents=self.app.tables.get('documents')

        model=ItemModel()
        model.itemChanged.connect(self.on_itemChanged)

        for d in documents:
            item=Item('document', d['id'], self.app.window)
            model.appendRow(item)

        self.setModel(model)
        self.app.window.activateTabWidget(self)
        self.setFocus()

    def on_itemChanged(self, item):
        self.app.tables.update('metadata', {'did':item.id()}, {'title':item.text().title()})

    def open(self):
        item=self.currentItem()
        if item is None: return

        filePath=self.app.tables.get('documents', {'id':item.id()}, 'loc')
        self.app.window.open(filePath)
        self.app.window.deactivateTabWidget(self)

    def close(self):
        self.app.deactivateTabWidget(self)
