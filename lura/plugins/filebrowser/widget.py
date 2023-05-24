import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from plugin.widget import TreeWidget

class EmptyIconProvider(QFileIconProvider):

    def icon(self, _): return QIcon()

class Tree(TreeWidget):

    openWanted=pyqtSignal(str, bool)

    def __init__(self):

        super().__init__()

        model=QFileSystemModel()
        model.setIconProvider(EmptyIconProvider())
        self.setModel(model)
        self.setPath(os.path.abspath('.'))

        for i in range(0, 4): self.hideColumn(i)

    def setPath(self, path=None):

        if path is None: path = os.path.abspath('.')
        self.model().setRootPath(path)
        self.setRootIndex(self.model().index(path))

    def keyPressEvent(self, event):

        if event.modifiers():
            if event.key()==Qt.Key_O:
                self.openWanted.emit('reset', False)
            elif event.key()==Qt.Key_S:
                self.openWanted.emit('below', False)
            else:
                super().keyPressEvent(event)
        else:
            if event.key()==Qt.Key_O:
                self.openWanted.emit('reset', True)
            elif event.key()==Qt.Key_S:
                self.openWanted.emit('below', True)
            else:
                super().keyPressEvent(event)
