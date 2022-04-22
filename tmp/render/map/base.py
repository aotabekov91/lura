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
        self.m_proxy=QSortFilterProxyModel()
        self.m_proxy.setSourceModel(self.m_model)
        self.m_proxy.setDynamicSortFilter(True)
        self.connectModel()
        self.setup()

    def setup(self):
        self.m_proxy=QSortFilterProxyModel()
        self.m_proxy.setSourceModel(self.m_model)
        self.m_proxy.setDynamicSortFilter(True)

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

    def itemParent(self, item):
        if item is None: return self.invisibleRootItem()
        if item.parent() is None: return self.invisibleRootItem()
        return item.parent()

    def clear(self):
        for index in range(self.invisibleRootItem().rowCount()):
            self.invisibleRootItem().takeRow(index)
                
    def model(self):
        return self.m_model

    def proxy(self):
        return self.m_proxy
