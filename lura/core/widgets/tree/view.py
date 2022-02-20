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
    

class TreeView(QGraphicsView):

    buttonClicked=pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.m_parent = parent
        self.window = parent.window
        self.setScene(QGraphicsScene())
        self.setup()

    def setup(self):
        self.m_model=None
        self.m_currentItem = None
        self.expanded=[]
        self.yanked=[]
        self.copied=[]
        self.m_filteredOut=[]

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setActions()

    def resetFilter(self):
        for item in self.m_filteredOut:
            item.show()
        self.m_filteredOut=[]

    def filterOut(self, item):
        item.hide()
        self.m_filteredOut+=[item]

    def unfilter(self):
        self.resetFilter()
        self.updatePosition()

    def setActions(self):
        self.actions=[]
        global config
        for func, key in config.items():

            m_action=QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetShortcut)
            self.actions+=[m_action]
            m_action.triggered.connect(getattr(self, func))
            self.addAction(m_action)

    def reset(self):
        for item in self.yanked:
            self.unselect(item)
        for (item, copy) in self.copied:
            self.unselect(item)
        self.yanked=[]
        self.copied=[]
        self.highlight()

    def countLevel(self, item, level=1):
        if item in [None, self.m_root]: return level
        return self.countLevel(item.parent(), level+1)

    def setFixedWidth(self, item=None):

        if self.m_model is None: return
        if item is None: item=self.m_root

        if item is not self.m_root:
            width=self.m_parent.width()-15
            newWidth=max(25, width-25*self.countLevel(item))
            item.proxy().setFixedWidth(newWidth)

        for index in range(item.rowCount()):
            self.setFixedWidth(item.child(index))

    def currentItem(self):
        return self.m_currentItem

    def setCurrentItem(self, item):
        if self.m_currentItem is not None: self.unhighlight()
        self.m_currentItem = item
        self.highlight()
        if self.m_currentItem is not None:
            self.centerOn(self.m_currentItem.proxy().button())

    def unselect(self, item=None):
        if item is None: item = self.currentItem()
        item.proxy().setStyleSheetWidget("background-color: rgba(255, 255, 255, 0);")
        item.proxy().setStyleSheetButton("background-color: rgba(255, 255, 255, 0);")

    def select(self, item=None):
        if item is None: item = self.currentItem()
        item.proxy().setStyleSheetWidget('background-color:rgba(255, 211, 25, 55);')
        item.proxy().setStyleSheetButton("background-color: rgba(255, 211, 25, 55);")

    def unhighlight(self, item=None):
        if item is None: item = self.currentItem()
        if item in self.yanked or item in self.copied:
            self.select(item)
        else:
            item.proxy().setStyleSheetButton("background-color: rgba(255, 255, 255, 0);")
            item.proxy().widget().setStyleSheet("background-color: rgba(255, 255, 255, 0);")

    def highlight(self, item=None):
        if item is None: item = self.currentItem()
        item.proxy().setStyleSheetButton("background-color: rgba(255, 55, 55, 10);")
        item.proxy().widget().setStyleSheet("background-color: rgba(191, 209, 229, 55);")

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

    def pushButtonClicked(self, item):

        self.setCurrentItem(item)

        if item in self.expanded:
            self.collapse(item)
            self.expanded.pop(self.expanded.index(item))
        else:
            self.expand(item)
            self.expanded+=[item]

        self.buttonClicked.emit()
        self.updatePosition()

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

    def expand(self, m_item=False):
        if self.m_root.rowCount()==0: return
        if m_item is False:
            if self.currentItem() is None:
                m_item=self.m_root
            else:
                m_item = self.currentItem()

        for index in range(m_item.rowCount()):
            child=m_item.child(index)
            if not child in self.m_filteredOut: child.show()
        self.updatePosition()

    def collapse(self, m_item=False):
        if self.m_root.rowCount()==0: return
        if m_item is False:
            if self.currentItem() is None:
                m_item=self.m_root
            else:
                m_item = self.currentItem()

        for index in range(m_item.rowCount()):
            child = m_item.child(index)
            child.hide()
            self.collapse(child)
        self.updatePosition()


    def moveSiblingUp(self):
        if self.currentItem().row()==0: return
        parent=self.currentItem().parent()
        if parent is None: parent=self.model().invisibleRootItem()
        self.setCurrentItem(parent.child(self.currentItem().row()-1))

    def moveSiblingDown(self):
        parent=self.currentItem().parent()
        if parent is None: parent=self.model().invisibleRootItem()
        if parent.rowCount()==self.currentItem().row(): return
        self.setCurrentItem(parent.child(self.currentItem().row()+1))

    def makeRootItem(self):
        self.setRootItem(self.currentItem())

    def rootUp(self):
        item=self.currentItem()
        if not hasattr(item.parent(), 'parent'): return
        grandParent=item.parent().parent()
        if grandParent is None: grandParent=self.model().invisibleRootItem()
        self.setRootItem(grandParent)

    def setRootItem(self, item):
        self.m_root=item

        if not item.hasChildren(): 
            parent=item.parent()
            if parent is None: parent=self.m_model.invisibleRootItem()
            self.m_root=parent
            return

        for index in range(self.m_model.invisibleRootItem().rowCount()):
            self.m_model.invisibleRootItem().child(index).hide()

        for index in range(item.rowCount()):
            item.child(index).show()

        self.updatePosition()

        self.setCurrentItem(item.child(0))

    def yank(self):
        self.select(self.currentItem())
        self.yanked+=[self.currentItem()]

    def copy(self):
        self.select(self.currentItem())
        self.copied+=[(self.currentItem(), self.currentItem().copy())]

    def pasteBelow(self):
        for yanked in self.yanked:
            self.unselect(yanked)
            self.model().itemParent(yanked).takeRow(yanked.row())
            item=self.currentItem()
            self.model().itemParent(item).insertRow(item.row()+1, yanked)
        for (original, copy) in self.copied:
            self.unselect(original)
            item=self.currentItem()
            self.model().itemParent(item).insertRow(item.row()+1, copy)
        self.updatePosition()
        self.yanked=[]
        self.copied=[]

    def pasteInside(self):
        for yanked in self.yanked:
            self.unselect(yanked)
            self.model().itemParent(yanked).takeRow(yanked.row())
            item=self.currentItem()
            item.insertRow(item.rowCount(), yanked)
        for (original, copy) in self.copied:
            self.unselect(original)
            item=self.currentItem()
            item.insertRow(item.rowCount(), copy)
        self.updatePosition()
        self.yanked=[]
        self.copied=[]
        self.setFocus()

    def pasteAbove(self):
        for yanked in self.yanked:
            self.unselect(yanked)
            self.model().itemParent(yanked).takeRow(yanked.row())
            item=self.currentItem()
            row=(item.row()-1)*(item.row()!=0)
            self.model().itemParent(item).insertRow(row, yanked)
        for (original, copy) in self.copied:
            self.unselect(original)
            item=self.currentItem()
            row=(item.row()-1)*(item.row()!=0)
            self.model().itemParent(item).insertRow(row, copy)
        self.updatePosition()
        self.yanked=[]
        self.copied=[]

    def delete(self):
        if len(self.yanked)>0:
            for item in self.yanked:
                self.model().itemParent(item).takeRow(item.row())
        else:
            item=self.currentItem()
            self.model().itemParent(item).takeRow(item.row())
        self.setFocus()

    def moveToParent(self):
        if self.currentItem().parent() is None: return
        self.setCurrentItem(self.currentItem().parent())
