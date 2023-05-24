import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import watch
from lura.utils import Plugin
from lura.utils.widgets import Tree

class EmptyIconProvider(QFileIconProvider):
    def icon(self, _):
        return QIcon()

class FileBrowser(Plugin):

    def __init__(self, app):
        super().__init__(app)

        self.tree=Tree(app, self, 'left', 'File browser')
        self.tree.keyPressEventOccurred.connect(self.on_treeKeyPress)
        self.setup()

    def setup(self):
        model=QFileSystemModel()
        model.setIconProvider(EmptyIconProvider())
        self.tree.setModel(model)
        for i in range(1, 4):
            self.tree.hideColumn(i)
        self.setPath(os.path.abspath('.'))

    def on_treeKeyPress(self, event):
        if event.modifiers() and event.key()==Qt.Key_O: 
            self.openBelowFocus()
        elif event.key()==Qt.Key_O:
            self.open()
        elif event.key()==Qt.Key_I:
            self.openBelow()
        else:
            super().keyPressEvent(event)

    def deactivate(self):
        self.activated=False
        self.tree.deactivate()

    @watch(widget='window', context=Qt.WindowShortcut)
    def toggle(self):
        if not self.activated:
            self.activated=True
            self.tree.activate()
        else:
            self.deactivate()

    def open(self):
        path=self.currentPath()
        if path and os.path.isdir(path): 
            self.tree.expand(self.tree.currentIndex())
        else:
            self.app.window.open(path)

    def openBelowFocus(self):
        path=self.currentPath()
        if path and os.path.isfile(path): 
            self.app.window.open(path, how='below')

    def openBelow(self):
        path=self.currentPath()
        if path and os.path.isfile(path): 
            self.app.window.open(path, how='below', focus=False)

    def setPath(self, path=None):
        if path is None: path = os.path.abspath('.')
        self.tree.model().setRootPath(path)
        self.tree.setRootIndex(self.tree.model().index(path))

    def currentPath(self):
        if self.tree.currentIndex():
            return self.tree.model().filePath(self.tree.currentIndex())
