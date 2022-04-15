import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core import MapTree

class TreeFileBrowser(MapTree):

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.m_parent=parent
        self.window = parent.window
        self.setup()

    def setup(self):
        self.m_model = QFileSystemModel()
        self.setModel(self.m_model)

        self.header().hide()
        for i in range(1, 4):
            self.hideColumn(i)

    def tree(self, path=None):

        if path is None: path = os.path.abspath('.')

        self.m_model.setRootPath(path)
        self.setRootIndex(self.m_model.index(path))
        self.setFocus()

    def expand(self):
        currentIndex = self.currentIndex()
        path = self.m_model.filePath(currentIndex)
        if not self.m_model.isDir(currentIndex):
            self.window.open(path)
        else:
            super().expand()

    def makeRoot(self):
        self.m_model.setRootPath(self.m_model.filePath(self.currentIndex()))
        self.setRootIndex(self.currentIndex())
        self.setFocus()

    def rootUp(self):
        path=self.m_model.rootPath()
        if not '/' in path: return
        parent=path.rsplit('/', 1)[0]
        self.m_model.setRootPath(parent)
        self.setRootIndex(self.m_model.index(parent))
        self.setFocus()

    def currentPath(self):
        if self.currentIndex() is None: return
        return self.m_model.filePath(self.currentIndex())
