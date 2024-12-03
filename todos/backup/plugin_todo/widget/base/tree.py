from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TreeWidget(QTreeView):

    openWanted=pyqtSignal()
    hideWanted=pyqtSignal()
    returnPressed=pyqtSignal()

    itemChanged=pyqtSignal(object)
    indexChanged=pyqtSignal(object)
    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, *args, **kwargs): 

        super().__init__(*args, **kwargs)

        self.setHeaderHidden(True)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setUI()

    def setUI(self):

        self.style_sheet = '''
            QTreeView{
                border-width: 0px;
                color: transparent;
                border-color: transparent; 
                background-color: transparent; 
                show-decoration-selected: 0;
                }

            QTreeView::item{
                color: white;
                border-color: transparent;
                background-color: transparent;
                border-radius: 10px;
                border-style: outset;
                padding: 5px 5px 5px 10px;
                }
            QTreeView::item:selected:active {
                border-color: red;
                border-width: 2px;
                }
                '''

        self.setStyleSheet(self.style_sheet)

    def currentItem(self):

        if self.model():
            if type(self.model())==QStandardItemModel:
                return self.model().itemFromIndex(self.currentIndex())
            elif hasattr(self.model(), 'itemFromIndex'):
                return self.model().itemFromIndex(self.currentIndex())
            elif type(self.model())==QSortFilterProxyModel:
                index=self.model().mapToSource(self.currentIndex())
                return self.model().itemFromIndex(index)

    def moveUp(self):

        if self.currentIndex(): self.customMove('MoveUp')

    def moveDown(self):

        if self.currentIndex(): self.customMove('MoveDown')

    def expand(self, index=None):

        if index: self.setCurrentIndex(index)
        super().expand(self.currentIndex())

    def expandAllInside(self, item=None):

        if item is None: item=self.currentItem()
        if item is None: return
        super().expand(item.index())
        for i in range(item.rowCount()):
            self.expandAllInside(item.child(i))

    def expandAll(self, index=None):

        if index is None:
            super().expandAll()
        elif index.isValid():
            if not self.isExpanded(index): self.expand(index)
            for row in range(self.model().rowCount()):
                self.expandAll(index.child(row,0))

    def expandAbove(self, child):

        index=child.parent()
        while index.isValid():
            index=index.parent()
            self.expand(index)

    def collapseAll(self, index=None):

        if index is not None and index.isValid():
            if not self.isExpanded(index):
                self.collapse(index)
            for row in range(self.model().rowCount()):
                self.collapseAll(index.child(row,0))
        else:
            super().collapseAll()

    def collapseAllInside(self, item=None):

        if item is None: item=self.currentItem()
        if item is None: return
        super().collapse(item.index())
        for i in range(item.rowCount()):
            self.collapseAllInside(item.child(i))

    def collapse(self, index=None):

        if index is None: index=self.currentIndex()
        if index: super().collapse(index)

    def rootDown(self):

        index=self.currentIndex()
        if index:
            self.setRootIndex(index)
            child=index.child(0,0)
            if child.isValid(): self.setCurrentIndex(child)

    def rootUp(self):

        index=self.rootIndex()
        if index.parent().isValid():
            self.setRootIndex(index.parent())
            self.setCurrentIndex(index)

    def customMove(self, direction):

        action=getattr(QAbstractItemView, direction)
        ind=self.moveCursor(action, Qt.NoModifier)
        self.setCurrentIndex(ind)

    def gotoStart(self):

        index=self.rootIndex()
        if index: self.setCurrentIndex(index.child(0, 0))

    def gotoParent(self):

        index=self.currentIndex()
        parent=index.parent()
        if parent.isValid(): self.setCurrentIndex(parent)

    def gotoSibling(self, kind='up'):

        index=self.currentIndex()
        parent=index.parent()

        if kind=='up':
            new=parent.child(index.row()-1, 0)
        else:
            new=parent.child(index.row()+1, 0)
        if new.isValid(): self.setCurrentIndex(new )

    def gotoEnd(self): 

        index=self.currentIndex()
        if index:
            parent=index.parent()
            last=parent.child(index.model().rowCount(parent)-1, 0)
            self.setCurrentIndex(last)

    def keyPressEvent(self, event):

        self.keyPressEventOccurred.emit(event)

        if event.key()==Qt.Key_J:
            self.moveDown()
        elif event.text()=='G':
            self.gotoEnd()
        elif event.key()==Qt.Key_G:
            self.gotoStart()
        elif event.key()==Qt.Key_BracketLeft:
            self.gotoSibling(kind='up')
        elif event.key()==Qt.Key_BracketRight:
            self.gotoSibling(kind='down')
        elif event.key()==Qt.Key_P:
            self.gotoParent()
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
        elif event.key()==Qt.Key_D:
            self.rootDown()
        elif event.key()==Qt.Key_Semicolon:
            self.moveToParent()
        elif event.key()==Qt.Key_B:
            self.moveToBottom()
        elif event.key()==Qt.Key_X:
            self.expandAllInside()
        elif event.key()==Qt.Key_T:
            self.collapseAllInside()
        elif event.key()==Qt.Key_O:
            self.openWanted.emit()
        elif event.key()==Qt.Key_Escape:
            self.hideWanted.emit()
        elif event.key()==Qt.Key_Return:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)

    def setCurrentIndex(self, index):

        super().setCurrentIndex(index)
        if self.model() is None: return
        if self.currentItem() is None: return
        self.indexChanged.emit(index)
        self.itemChanged.emit(self.currentItem())

    def event(self, event):

        if event.type()==QEvent.Enter:
            item=self.currentItem()
            if item: self.itemChanged.emit(item)
        return super().event(event)
