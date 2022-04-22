import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core import MapTree

class FileBrowser(MapTree):

    def __init__(self, parent, settings):
        super().__init__(parent, parent)
        self.window = parent
        self.location = 'left'
        self.name = 'fileBrowser'

        self.globalKeys = {
            'Ctrl+f': (
                self.toggle,
                self.window,
                Qt.WindowShortcut)
        }
        self.setup()

    def setup(self):

        self.path = os.path.abspath('.')

        self.setModel(QFileSystemModel())
        self.header().hide()

        for i in range(1, 4):
            self.hideColumn(i)

        self.window.setTabLocation(self, self.location, self.name)

    def toggle(self):

        if not self.isVisible():

            self.window.activateTabWidget(self)
            self.tree(self.path)
            self.setFocus()

        else:

            self.window.deactivateTabWidget(self)

    def open(self):
        self.window.open(self.currentPath())

    def tree(self, path=None):

        if path is None: path = os.path.abspath('.')

        self.model().setRootPath(path)
        self.setRootIndex(self.model().index(path))
        self.setFocus()

    def currentPath(self):
        if self.currentIndex() is None: return
        return self.model().filePath(self.currentIndex())
