from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from plugin.widget import TreeWidget

class OutlineTree(TreeWidget):
    
    def __init__(self, *args, **kwargs):

        super(OutlineTree, self).__init__(*args, **kwargs)

        self.m_expansionRole=Qt.UserRole+4
        self.m_expansionIDRole=Qt.UserRole+5

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.header().setSectionResizeMode(QHeaderView.Interactive)

    def restoreExpansion(self, index):

        if index.isValid():
            expanded=self.model().data(index, self.m_expansionRole)
            if self.isExpanded(index)!=expanded:
                self.setExpanded(index, expanded)
        for row in self.model().rowCount(index):
            self.restoreExpansion(self.model().index(row, 0, index))

    def synchronizeOutlineView(self, currentPage, outlineModel, parent):

        for row in range(outlineModel.rowCount(parent)):
            index=outlineModel.index(row, 0, parent)
            page=outlineModel.data(index, Qt.UserRole+1)
            if page==currentPage: return index
        for row in range(outlineModel.rowCount(parent)):
            index=outlineModel.index(row, 0, parent)
            match=self.synchronizeOutlineView(currentPage, outlineModel, index)
            if match.isValid():
                return match
        return QModelIndex()
