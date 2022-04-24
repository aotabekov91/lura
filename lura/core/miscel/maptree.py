from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.miscel import Item

class MapTree(QTreeView):

    returnPressed=pyqtSignal(object, object)
    currentItemChanged=pyqtSignal(QStandardItem)

    def __init__(self, parent, window):
        super().__init__(parent)

        self.window=window
        self.initialize()

    def initialize(self):

        self.yanked=[]
        self.copied=[]
        self.m_model=None
        self.m_proxy=None
        self.proxySet=False

        self.header().hide()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
        elif event.key()==Qt.Key_Z:
            self.update()
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
        elif event.key()==Qt.Key_Semicolon:
            self.moveToParent()
        elif event.key()==Qt.Key_B:
            self.moveToBottom()
        elif event.key()==Qt.Key_O:
            self.open()
        elif event.key()==Qt.Key_X:
            self.expandAllInside()
        elif event.key()==Qt.Key_T:
            self.collapseAllInside()
        elif event.key()==Qt.Key_Escape:
            if self.proxySet:
                self.deactivateFiltering()
            else:
                self.close()
        elif event.key()==Qt.Key_Return:
            self.returnPressed.emit(self.model(), self.currentIndex())
        elif event.key()==Qt.Key_F:
            self.activateFiltering()
        elif event.key()==Qt.Key_V:
            self.activateSorting()
        elif event.key()==Qt.Key_W:
            self.watch()

    def setCurrentIndex(self, index):
        super().setCurrentIndex(index)
        if self.model() is None: return
        if self.currentItem() is None: return
        self.currentItemChanged.emit(self.currentItem())

    def moveToParent(self):
        if self.currentItem().parent() is None: return
        self.setCurrentIndex(self.currentItem().parent().index())

    def moveToBottom(self):
        item=self.currentItem()
        if item is None: return
        parent=item.parent()
        if parent is None: 
            parent=self.model().invisibleRootItem()
        self.setCurrentIndex(parent.child(parent.rowCount()-1).index())

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
        temp=self.copied+self.yanked
        if len(temp)==0: return

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

        self.expand(item.index())
        self.setCurrentIndex(temp[0].index())

    def pasteBelow(self):
        temp=self.copied+self.yanked
        if len(temp)==0: return

        item=self.currentItem()
        if item is None: return
        itemParent=item.parent()
        if itemParent is None:
            itemParent=self.model().invisibleRootItem()
        for i in self.copied:
            itemParent.insertRow(item.row()+1, i)
        self.copied=[]

        for i in self.yanked:
            parent=i.parent()
            if parent is None: parent=self.model().invisibleRootItem()
            parent.takeRow(i.row())
            itemParent.insertRow(item.row()+1, i)
        self.yanked=[]

        self.setCurrentIndex(temp[0].index())

    def pasteAbove(self):
        temp=self.copied+self.yanked
        if len(temp)==0: return

        item=self.currentItem()
        if item is None: return
        itemParent=item.parent()
        if itemParent is None:
            itemParent=self.model().invisibleRootItem()
        row=item.row()

        for i in self.copied:
            itemParent.insertRow(row-1, i)

        self.copied=[]

        for i in self.yanked:
            parent=i.parent()
            if parent is None: parent=self.model().invisibleRootItem()
            parent.takeRow(i.row())
            itemParent.insertRow(row-1, i)
        self.yanked=[]

        self.setCurrentIndex(temp[0].index())

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

    def setProxyModel(self):
        super().setModel(self.m_proxy)

    def setModel(self, model):
        self.m_model=model
        if hasattr(model, 'proxy'):
            self.m_proxy=self.m_model.proxy()
        else:
            self.m_proxy=None
        super().setModel(model)
        if not hasattr(self.model(), 'invisibleRootItem'): return
        if self.model().invisibleRootItem().rowCount()>0:
            first=self.model().invisibleRootItem().child(0)
            if first is None: return
            self.setCurrentIndex(first.index())

    def open(self, item=None):

        if item is None: item = self.currentItem()
        if item is None: return

        if item.kind() == 'annotation':

            b = item.get('position').split(':')
            topLeft = QPointF(float(b[0]), float(b[1]))
            did = item.get('did')
            pageNumber = item.get('page')
            filePath = self.window.plugin.tables.get(
                'documents', {'id': did}, 'loc')

            self.window.open(filePath)
            self.window.view().jumpToPage(
                pageNumber, topLeft.x(), 0.95*topLeft.y())

        elif item.kind() == 'document':

            filePath = self.window.plugin.tables.get(
                'documents', {'id': item.id()}, 'loc')
            self.window.open(filePath)

    def close(self):
        pass

    def watch(self):
        pass

    def update(self):
        pass

    def activateSorting(self):
        if self.m_proxy is None: return
        item=self.currentItem()
        self.setProxyModel()
        index=self.m_proxy.mapFromSource(item.index())
        self.setCurrentIndex(index)
        self.proxySet=True
        self.sortByColumn(0, Qt.AscendingOrder)
        self.setFocus()

    def deactivateSorting(self):
        if self.m_proxy is None: return
        self.setModel(self.m_model)
        self.proxySet=False
        self.setFocus()

    def activateFiltering(self):
        if self.m_proxy is None: return
        item=self.currentItem()
        self.setProxyModel()
        index=self.m_proxy.mapFromSource(item.index())
        self.setCurrentIndex(index)
        self.proxySet=True
        self.window.plugin.command.activateCustom(
                lambda text: self._activateFiltering(text, True), 'Filter: ', self._activateFiltering)

    def _activateFiltering(self, text, final=False):
        if self.m_proxy is None: return
        self.m_proxy.setFilterRegExp(text)
        if final: self.setFocus()

    def deactivateFiltering(self):
        if self.m_proxy is None: return
        self.setModel(self.m_model)
        self.proxySet=False
        self.setFocus()

    def event(self, event):
        if event.type()==QEvent.Enter:
            item=self.currentItem()
            if item is not None:
                self.currentItemChanged.emit(item)
        return super().event(event)

    def document(self):
        return self.model()
