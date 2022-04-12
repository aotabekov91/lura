from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CustomTreeMap(QTreeView):

    def currentItem(self):
        return self.model().itemFromIndex(self.currentIndex())

    def moveUp(self):
        if self.currentIndex() is None: return
        self.customMove('MoveUp')

    def moveDown(self):
        if self.currentIndex() is None: return
        self.customMove('MoveDown')

    def expand(self):
        if self.currentIndex() is None: return
        super().expand(self.currentIndex())

    def collapse(self):
        if self.currentIndex() is None: return
        super().collapse(self.currentIndex())

    def makeRoot(self):
        if self.currentIndex() is None: return
        self.setRootIndex(self.currentIndex())

    def rootUp(self):
        if self.currentIndex() is None: return

        item=self.model().itemFromIndex(self.currentIndex())

        if not hasattr(self.parent(), 'parent'): return
        if not hasattr(self.parent().parent(), 'index'): return 

        self.setRootIndex(item.parent().parent().index())

    def customMove(self, direction):
        action=getattr(QAbstractItemView, direction)
        ind=self.moveCursor(action, Qt.NoModifier)
        self.setCurrentIndex(ind)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_J:
            self.moveDown()
        elif event.key()==Qt.Key_K:
            self.moveUp()
        elif event.key()==Qt.Key_L:
            self.expand()
        elif event.key()==Qt.Key_H:
            self.collapse()
        elif event.key()==Qt.Key_U:
            self.rootUp()
        elif event.key()==Qt.Key_R:
            self.makeRoot()
