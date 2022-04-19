from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.miscel import Item

class MapTree(QTreeView):

    currentItemChanged=pyqtSignal(QStandardItem)

    def __init__(self, parent, window):
        super().__init__(parent)

        self.window=window
        self.yanked=[]
        self.copied=[]

        self.setup()

    def setup(self):
        self.header().hide()

    def currentItem(self):
        if not self.isProxyModel:
            return self.model().itemFromIndex(self.currentIndex())
        else:
            index=self.model().mapToSource(self.currentIndex())
            return self.m_model.itemFromIndex(index)

    def moveUp(self):
        if self.currentIndex() is None: return
        self.customMove('MoveUp')

    def moveDown(self):
        if self.currentIndex() is None: return
        self.customMove('MoveDown')

    def expand(self, index=None):
        if index is None:
            if self.currentIndex() is None: return
            index=self.currentIndex()
        super().expand(self.currentIndex())

    def collapse(self):
        if self.currentIndex() is None: return
        super().collapse(self.currentIndex())

    def makeRoot(self):
        if self.currentIndex() is None: return
        self.setRootIndex(self.currentIndex())
        if hasattr(self.model(), 'setRootPath'):
            path=self.model().filePath(self.currentIndex())
            self.model().setRootPath(path)

    def rootUp(self):
        if hasattr(self.model(), 'itemFromIndex'):
            rootItem=self.model().itemFromIndex(self.rootIndex())
            if rootItem is None: return
            parent=rootItem.parent()
            if parent is None: parent=self.model().invisibleRootItem()
            self.setRootIndex(parent.index())
        elif hasattr(self.model(), 'rootPath'):
            path=self.model().rootPath()
            if not '/' in path: return
            parent=path.rsplit('/', 1)[0]
            self.model().setRootPath(parent)
            self.setRootIndex(self.model().index(parent))

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
        elif event.key()==Qt.Key_Y:
            self.yank()
        elif event.key()==Qt.Key_C:
            self.copy()
        elif event.key()==Qt.Key_I:
            self.pasteInside()
        elif event.key()==Qt.Key_P:
            self.pasteBelow()
        elif event.key()==Qt.Key_D:
            self.delete()
        elif event.key()==Qt.Key_A:
            self.addNode()
        elif event.key()==Qt.Key_E:
            self.edit(self.currentIndex())
        elif event.key()==Qt.Key_B:
            self.moveToParent()
        elif event.key()==Qt.Key_F:
            self.moveToUncle()
        elif event.key()==Qt.Key_O:
            self.open()

    def setCurrentIndex(self, index):
        super().setCurrentIndex(index)
        self.currentItemChanged.emit(self.currentItem())

    def moveToParent(self):
        if self.currentItem().parent() is None: return
        self.setCurrentIndex(self.currentItem().parent().index())

    def moveToUncle(self):
        item=self.currentItem()
        parent=item.parent()
        if parent is None: return
        if parent.rowCount()==item.row()+1: return
        self.setCurrentIndex(parent.child(item.row()+1).index())

    def delete(self, item=None):
        if item is None: item=self.currentItem()
        parent=item.parent()
        if parent is None: parent=self.model().invisibleRootItem()
        parent.takeRow(item.row())

    def yank(self):
        if self.currentItem() is None: return
        self.yanked+=[self.currentItem()]

    def copy(self):
        if self.currentItem() is None: return
        self.copied+=[self.currentItem().copy()]

    def pasteInside(self):
        if self.currentItem() is None: return
        item=self.currentItem()
        for i in self.copied:
            item.appendRow(i)
        self.copied=[]
        for i in self.yanked:
            parent=i.parent()
            if parent is None: parent=self.model().invisibleRootItem()
            parent.takeRow(i.row())
            item.appendRow(i)
        self.yanked=[]

    def pasteBelow(self):
        if self.currentItem() is None: return
        itemParent=item.parent()
        if itemParent is None:
            itemParent=self.model().invisibleRootItem()
        raise

    def pasteAbove(self):
        if self.currentItem() is None: return
        raise

    def addNode(self, item=None):
        if item is None: 
            temp=self.currentItem()
            if temp is not None: item=temp.parent()
            if item is None: item=self.model().invisibleRootItem()
        new=Item('container', None, self.window, 'Container')
        row=0
        if temp is not None: row=temp.row()+1
        item.insertRow(row, new)
        self.setCurrentIndex(new.index())

    def setProxyModel(self, model):
        self.m_proxy=model
        self.isProxyModel=True
        super().setModel(model)

    def setModel(self, model):
        self.m_model=model
        self.isProxyModel=False
        super().setModel(model)
        if not hasattr(self.model(), 'invisibleRootItem'): return
        if self.model().invisibleRootItem().rowCount()>0:
            first=self.model().invisibleRootItem().child(0)
            self.setCurrentIndex(first.index())

    def open(self):
        pass
