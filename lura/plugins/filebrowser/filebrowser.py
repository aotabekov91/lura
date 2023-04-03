import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin
from lura.utils.widgets import TreeView

class EmptyIconProvider(QFileIconProvider):
    def icon(self, _):
        return QIcon()

class FileBrowser(Plugin):

    def __init__(self, app):
        super().__init__(app, name='fileBrowser')

        self.tree=TreeView(app, self, location='left', name='fileBrowser')
        self.setup()

    def setup(self):
        model=QFileSystemModel()
        model.setIconProvider(EmptyIconProvider())
        self.tree.setModel(model)
        for i in range(1, 4):
            self.tree.hideColumn(i)
        self.set_path(os.path.abspath('.'))

    def deactivate(self):
        self.activated=False
        self.tree.deactivate()

    def activate(self):
        if not self.activated:
            self.activated=True
            self.tree.activate()
        else:
            self.deactivate()

    def open(self):
        path=self.currentPath()
        if path: self.app.window.open(path)

    def set_path(self, path=None):
        if path is None: path = os.path.abspath('.')
        self.tree.model().setRootPath(path)
        self.tree.setRootIndex(self.tree.model().index(path))

    def currentPath(self):
        if self.tree.currentIndex():
            return self.tree.model().filePath(self.tree.currentIndex())
