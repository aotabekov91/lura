import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.widget import InputTree

class EmptyIconProvider(QFileIconProvider):

    def icon(self, _): return QIcon()

class Tree(InputTree):

    openWanted=pyqtSignal(str, bool)

    def __init__(self):

        super().__init__()

        model=QFileSystemModel()
        model.setIconProvider(EmptyIconProvider())
        self.tree.setModel(model)
        self.setPath(os.path.abspath('.'))

        self.input.hide()
        for i in range(1, 4): self.tree.hideColumn(i)

    def setPath(self, path=None):

        if path is None: path = os.path.abspath('.')
        self.tree.model().setRootPath(path)
        self.tree.setRootIndex(self.tree.model().index(path))

    def keyPressEvent(self, event):

        if event.key()==Qt.Key_O:
            self.openWanted.emit('reset', False)
        elif event.key()==Qt.Key_S:
            self.openWanted.emit('below', False)
        else:
            super().keyPressEvent(event)
