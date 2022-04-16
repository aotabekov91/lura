from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class BaseMapDocument(QObject):

    rowsInserted = pyqtSignal('QModelIndex', int, int)
    rowsRemoved = pyqtSignal('QModelIndex', int, int)
    rowsMoved = pyqtSignal('QModelIndex', int, int)
    rowsAboutToBeRemoved = pyqtSignal('QModelIndex', int, int)
    dataChanged = pyqtSignal('QModelIndex')
    modelChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.m_model = QStandardItemModel()
        self.connectModel()

    def id(self):
        return self.m_id

    def setId(self, did):
        self.m_id=did

    def itemFromIndex(self, index):
        return self.m_model.itemFromIndex(index)

    def appendRow(self, item):
        self.m_model.invisibleRootItem().appendRow(item)

    def invisibleRootItem(self):
        return self.m_model.invisibleRootItem()

    def connectModel(self):

        self.m_model.rowsInserted.connect(self.rowsInserted)
        self.m_model.rowsRemoved.connect(self.rowsRemoved)
        self.m_model.rowsMoved.connect(self.rowsMoved)
        self.m_model.rowsAboutToBeRemoved.connect(self.rowsAboutToBeRemoved)
        self.m_model.dataChanged.connect(self.dataChanged)

    def findOrCreateContainer(self, title, item=None):
        if item is None: item=self.invisibleRootItem()

        containers=self.findContainer(title, item)
        if len(containers)>0: 
            if len(containers)>1: raise
            return containers[0]

    def findContainer(self, title, item):

        found=[]
        for index in range(item.rowCount()):
            child=item.child(index)

            cond1=child.itemData().kind()=='container'
            cond2=child.itemData().title()==title
            if cond1 and cond2: found+=[child]

        return found

    def isChild(self, item, parent):

        for index in range(parent.rowCount()):
            if parent.child(index).isEqual(item): return True
        return False

    def isIn(self, item, parent):
        if parent!=self.invisibleRootItem():
            if parent.itemData().kind()==item.itemData().kind():
                if parent.itemData().id()==item.itemData().id():
                    return True

        for index in range(parent.rowCount()):
            if self.isIn(item, parent.child(index)): return True
        return False

    def findItemByKind(self, kind, item=None, found=[]):
        if item is None: item=self.invisibleRootItem()

        if item != self.invisibleRootItem():
            if item.itemData().kind()==kind: found+=[item]

        for index in range(item.rowCount()):
            self.findItemByKind(kind, item.child(index), found)

        return found

    def itemParent(self, item):
        if item is None: return self.invisibleRootItem()
        if item.parent() is None: return self.invisibleRootItem()
        return item.parent()

    def clear(self):
        for index in range(self.invisibleRootItem().rowCount()):
            self.invisibleRootItem().takeRow(index)
