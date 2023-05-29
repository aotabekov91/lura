from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core import MapTree

class Outline(MapTree):
    
    def __init__(self, parent, settings):
        super().__init__(parent, parent)
        self.window=parent
        self.s_settings=settings
        self.location='left'
        self.name='outline'
        self.globalKeys={
                'Ctrl+o': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.outlines={}

        self.m_expansionRole=Qt.UserRole+4
        self.m_expansionIDRole=Qt.UserRole+5

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.documentRegistered.connect(self.register)
        self.window.currentPageChanged.connect(self.on_currentPageChanged)

        self.expanded.connect(self.on_expanded)
        self.collapsed.connect(self.on_collapsed)
        self.header().setSectionResizeMode(QHeaderView.Interactive)
        self.header().hide()

        self.clicked.connect(self.on_outline_clicked)
        self.window.setTabLocation(self, self.location, self.name)

    def on_outline_clicked(self, index):

        page=index.data(Qt.UserRole+1)
        left=index.data(Qt.UserRole+2)
        top=index.data(Qt.UserRole+3)

        self.window.view().jumpToPage(page, left, top)

    def expandAll(self, index=None):
        if index is None:
            super().expandAll()
        elif index.isValid():
            if not self.isExpanded(index):
                self.expand(index)

            for row in range(self.model().rowCount()):

                self.expandAll(index.child(row,0))


    def collapseAll(self, index=None):

        if index is not None and index.isValid():
            if not self.isExpanded(index):
                self.collapse(index)

            for row in range(self.model().rowCount()):

                self.collapseAll(index.child(row,0))

        else:

            super().collapseAll()


    def on_expanded(self, index):
        self.model().setData(index, True, self.m_expansionRole)

    def on_collapsed(self, index):
        self.model().setData(index, False, self.m_expansionRole)

    def on_currentPageChanged(self, document, page):

        outline=self.outlines.get(document, None)

        if outline is None: return

        found=self.synchronizeOutlineView(page, outline, QModelIndex()) 
        if found.isValid():
            self.setCurrentIndex(found)

    def expandAbove(self, child):

        index=child.parent()
        while index.isValid():
            index=index.parent()
            self.expand(index)

    def restoreExpansion(self, index):

        if index.isValid():
            expanded=self.model().data(index, self.m_expansionRole)

            if isExpanded(index)!=expanded:
                self.setExpanded(index, expanded)

        for row in self.model().rowCount(index):
            self.restoreExpansion(self.model().index(row, 0, index))


    def synchronizeOutlineView(self, currentPage, outlineModel, parent):

        for row in range(outlineModel.rowCount(parent)):

            index=outlineModel.index(row, 0, parent)
            page=outlineModel.data(index, Qt.UserRole+1)

            if page==currentPage:
                return index

        for row in range(outlineModel.rowCount(parent)):

            index=outlineModel.index(row, 0, parent)
            match=self.synchronizeOutlineView(currentPage, outlineModel, index)

            if match.isValid():
                return match

        return QModelIndex()


    def toggle(self, forceShow=False):

        if self.window.view() is None: return

        if not self.isVisible():

            document=self.window.view().document()
            outline=self.outlines.get(document, None)
            if outline is None: return

            self.setModel(outline)
            self.window.activateTabWidget(self)
            self.show()
            self.setFocus()

        else:

            self.window.deactivateTabWidget(self)

    def on_viewChanged(self, view):
        if not self.isVisible(): return
        document=view.document()
        outline=self.outlines.get(document, None)
        if not outline: self.setModel(outline)

    def open(self):
        index=self.currentIndex()

        page=index.data(Qt.UserRole+1)
        left=index.data(Qt.UserRole+2)
        top=index.data(Qt.UserRole+3)

        self.window.view().jumpToPage(page, left, top)
        self.window.view().setFocus()

    def register(self, document):
        outline=document.loadOutline()
        # outline.setHorizontalHeaderLabels(['Content', 'Page'])
        self.outlines[document]=outline

    def close(self):
        self.window.deactivateTabWidget(self)