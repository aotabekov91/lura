from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class EmptyIconProvider(QFileIconProvider):
    def icon(self, _):
        return QIcon()

class TreeView(QTreeView):

    keyPressEventOccurred=pyqtSignal(object)
    returnPressed=pyqtSignal(object, object)
    itemChanged=pyqtSignal(QStandardItem)

    def __init__(self, app, parent, location=None, name=None, model=None):
        super().__init__(app.window)
        self.app=app
        self.name=name
        self.m_model=model
        self.m_parent=parent
        self.location=location

        self.header().hide()
        self.app.window.docks.setTabLocation(self, self.location, self.name)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def deactivate(self):
        self.app.window.docks.deactivateTabWidget(self)

    def activate(self):
        self.app.window.docks.activateTabWidget(self)
        self.setFocus()

    def currentItem(self):
        if self.model() is None: return None

        if type(self.model())==QStandardItemModel:
            return self.model().itemFromIndex(self.currentIndex())
        elif hasattr(self.model(), 'itemFromIndex'):
            return self.model().itemFromIndex(self.currentIndex())
        elif type(self.model())==QSortFilterProxyModel:
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

    def expandAllInside(self, item=None):
        if item is None: item=self.currentItem()
        if item is None: return
        super().expand(item.index())
        for i in range(item.rowCount()):
            self.expandAllInside(item.child(i))

    def collapseAllInside(self, item=None):
        if item is None: item=self.currentItem()
        if item is None: return
        super().collapse(item.index())
        for i in range(item.rowCount()):
            self.collapseAllInside(item.child(i))

    def collapse(self, index=None):
        if index is None: index=self.currentIndex()
        if index: super().collapse(index)

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
            self.setCurrentIndex(self.model().index(0, 0))

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
        elif event.key()==Qt.Key_Z:
            self.update()
        elif event.key()==Qt.Key_R:
            self.makeRoot()
        elif event.key()==Qt.Key_Semicolon:
            self.moveToParent()
        elif event.key()==Qt.Key_B:
            self.moveToBottom()
        elif event.key()==Qt.Key_X:
            self.expandAllInside()
        elif event.key()==Qt.Key_T:
            self.collapseAllInside()
        elif event.key()==Qt.Key_Escape:
            self.close()
        elif event.key()==Qt.Key_Return:
            self.returnPressed.emit(self.model(), self.currentIndex())
        else:
            self.keyPressEventOccurred.emit(event)
            super().keyPressEvent(event)

    def setCurrentIndex(self, index):
        super().setCurrentIndex(index)
        if self.model() is None: return
        if self.currentItem() is None: return
        self.itemChanged.emit(self.currentItem())

    def setModel(self, model, iconProvider=EmptyIconProvider):
        super().setModel(model)
        self.m_model=model
        if not hasattr(self.model(), 'invisibleRootItem'): return
        if self.model().invisibleRootItem().rowCount()>0:
            first=self.model().invisibleRootItem().child(0)
            if first is None: return
            self.setCurrentIndex(first.index())

    def event(self, event):
        if event.type()==QEvent.Enter:
            item=self.currentItem()
            if item is not None:
                self.itemChanged.emit(item)
        return super().event(event)
    
