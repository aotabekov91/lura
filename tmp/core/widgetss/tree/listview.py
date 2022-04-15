from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

config={'moveDown': 'j',
        'moveUp': 'k',
        'moveSiblingDown': 'Shift+j',
        'moveSiblingUp': 'Shift+k',
        'moveToParent': 'Shift+h',
        'collapse': 'h',
        'expand': 'l',
        'copy': 'c',
        'yank': 'y',
        'pasteBelow': 'p',
        'pasteAbove': 'Shift+p',
        'pasteInside': 'i',
        'reset': 'Shift+r',
        'rootUp': 'u',
        'makeRootItem': 'r'}
    

class ListView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.m_parent = parent
        self.window = parent.window
        self.setScene(QGraphicsScene())
        self.setup()

    def setup(self):
        self.m_model=None
        self.m_currentItem = None

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setActions()

    def currentItem(self):
        return self.m_currentItem

    def setCurrentItem(self, item):
        if self.m_currentItem is not None: self.unhighlight()
        self.m_currentItem = item
        self.highlight()
        if self.m_currentItem is not None:
            self.centerOn(self.m_currentItem.proxy().button())

    def model(self):
        return self.m_model

    def setModel(self, document):
        self.m_model = document

        self.m_model.dataChanged.connect(self.on_dataChanged)
        self.m_model.rowsInserted.connect(self.on_rowsInserted)
        self.m_model.rowsRemoved.connect(self.on_rowsRemoved)
        self.m_model.rowsAboutToBeRemoved.connect(self.on_rowsAboutToBeRemoved)

        self.setRootItem(self.m_model.invisibleRootItem())

        self.addModelItems()
        self.updatePosition()

        if document.invisibleRootItem().rowCount() > 0:
            self.setCurrentItem(document.invisibleRootItem().child(0))

        for index in range(self.m_model.invisibleRootItem().rowCount()):
            self.collapse(self.m_model.invisibleRootItem().child(index))

    def on_dataChanged(self, index):
        self.updatePosition()

    def on_rowsRemoved(self, parentIndex, begin, end):
        self.updatePosition()

    def on_rowsAboutToBeRemoved(self, parentIndex, begin, end):
        if parentIndex.model() is None:
            item = self.m_model.invisibleRootItem().child(begin)
        else:
            item = self.m_model.itemFromIndex(parentIndex).child(begin)

        item.hide()
        self.remove(item)
        self.updatePosition()

    def remove(self, item):

        self.scene().removeItem(item.proxy().button())
        self.scene().removeItem(item.proxy())

        for index in range(item.rowCount()):
            self.remove(item.child(index))

    def on_rowsInserted(self, parentIndex, begin, end):
        return 
        if parentIndex.model() is None:
            item = self.m_model.invisibleRootItem().child(begin)
        else:
            item = self.m_model.itemFromIndex(parentIndex).child(begin)

        self.addNode(item)
        item.show()
        self.updatePosition()

    def addNode(self, m_item):

        self.scene().addItem(m_item.proxy().button())
        self.scene().addItem(m_item.proxy())

        m_item.proxy().sizeChanged.connect(self.updatePosition)
        m_item.proxy().pushButtonClicked.connect(self.pushButtonClicked)

        for index in range(m_item.rowCount()):
            self.addNode(m_item.child(index))

        self.setFixedWidth()

    def clear(self):
        for item in self.scene().items():
            self.scene().removeItem(item)

    def nextVisibleItem(self, item):
        if item.hasChildren():
            for index in range(item.rowCount()):
                child=item.child(index)
                if child.isVisible(): return child

        parent=item.parent()
        if parent is None: parent=self.m_root

        if item.row()+1<parent.rowCount(): return parent.child(item.row()+1)

        uncle=self.nextUncle(parent)
        if uncle is None: return item
        if uncle==self.m_root.child(0): return item
        return uncle

    def nextUncle(self, item):

        parent=item.parent()
        if not hasattr(item.parent(), 'rowCount'): parent=self.m_root
        if item.row()+1<parent.rowCount(): return parent.child(item.row()+1)
        if parent==self.m_root: return
        return self.nextUncle(parent)

    def lastVisibleItem(self, item):
        if item is None: return self.m_root.child(0)
        if not hasattr(item, 'hasChildren'): return item
        if not item.hasChildren(): return item
        if not item.child(0).isVisible(): return item
        return self.lastVisibleItem(item.child(item.rowCount()-1))

    def previousVisibleItem(self, item):
        if item.row()==0:
            if not item.parent() in [None, self.m_root]:
                return item.parent()
            return item
        if hasattr(item.parent(), 'child'):
            for index in range(item.row()-1, -1, -1):
                child=item.parent().child(index)
                if not child in self.m_filteredOut: return self.lastVisibleItem(child)
        return self.lastVisibleItem(self.m_root.child(item.row()-1))

    def updatePosition(self, m_item=None, initial=True):
        if initial: m_item=self.m_root

        if not m_item in [None, self.m_root]:

            if not m_item.isVisible(): return

            if m_item.row() == 0:
                if m_item.parent() in [self.m_root, None]:
                    m_item.proxy().setPos(25, 0)
                else:
                    x, y = m_item.parent().proxy().bottomLeft()
                    m_item.proxy().setPos(x+25, y)
            else:
                siblingUp=None
                parent=m_item.parent()
                if not hasattr(parent, 'child'): parent=self.m_root

                for index in range(m_item.row()-1, -1, -1):
                    upper=parent.child(index)
                    if not upper in self.m_filteredOut: 
                        siblingUp=upper
                        break

                if siblingUp is None:
                    x, y = m_item.parent().proxy().bottomLeft()
                    m_item.proxy().setPos(x+25, y)
                else:
                    lastVisibleProxy = self.lastVisibleProxy(siblingUp)
                    x, y = lastVisibleProxy.bottomLeft()
                    m_item.proxy().setPos(siblingUp.proxy().pos().x(), y)

            m_item.update()

        for index in range(m_item.rowCount()):
            self.updatePosition(m_item.child(index), initial=False)

    def lastVisibleProxy(self, item):
        if not item.hasChildren():
            return item.proxy()
        else:
            if not item.child(0).proxy().isVisible():
                return item.proxy()
            else:
                return self.lastVisibleProxy(item.child(item.rowCount()-1))

    def addModelItems(self):

        item = self.m_root

        for index in range(item.rowCount()):
            self.addNode(item.child(index))

    def customMove(self, kind):
        if self.m_currentItem is None:
            self.setCurrentItem(self.m_root.child(0))
        if kind == 'down':
            item = self.nextVisibleItem(self.currentItem())
            self.setCurrentItem(item)
        if kind == 'up':
            item = self.previousVisibleItem(self.currentItem())
            self.setCurrentItem(item)

    def moveDown(self):
        if self.m_root.rowCount()==0: return
        self.customMove('down')
        self.centerOn(self.m_currentItem.proxy().button())

    def moveUp(self):
        if self.m_root.rowCount()==0: return
        self.customMove('up')
        self.centerOn(self.m_currentItem.proxy().button())

    def delete(self):
        if len(self.yanked)>0:
            for item in self.yanked:
                self.model().itemParent(item).takeRow(item.row())
        else:
            item=self.currentItem()
            self.model().itemParent(item).takeRow(item.row())
        self.setFocus()
