import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin
from lura.utils.widgets import MapTree

class OutlineTree(MapTree):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.m_expansionRole=Qt.UserRole+4
        self.m_expansionIDRole=Qt.UserRole+5

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.expanded.connect(self.m_parent.on_expanded)
        self.collapsed.connect(self.m_parent.on_collapsed)

        self.header().setSectionResizeMode(QHeaderView.Interactive)
        self.clicked.connect(self.m_parent.on_outline_clicked)

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
            if page==currentPage:
                return index
        for row in range(outlineModel.rowCount(parent)):
            index=outlineModel.index(row, 0, parent)
            match=self.synchronizeOutlineView(currentPage, outlineModel, index)
            if match.isValid():
                return match
        return QModelIndex()

    def expandAbove(self, child):
        index=child.parent()
        while index.isValid():
            index=index.parent()
            self.expand(index)

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


class Outline(Plugin):
    
    def __init__(self, app):
        super().__init__(app, name='outline')

        self.outlines={}
        self.tree=OutlineTree(app, self, 'left', 'outline')

        self.app.window.viewChanged.connect(self.on_viewChanged)
        self.app.buffer.documentCreated.connect(self.register)
        self.app.window.currentPageChanged.connect(self.on_currentPageChanged)

    def on_outline_clicked(self, index):
        page=index.data(Qt.UserRole+1)
        left=index.data(Qt.UserRole+2)
        top=index.data(Qt.UserRole+3)
        self.app.window.view().jumpToPage(page, left, top)

    def on_expanded(self, index):
        self.tree.model().setData(index, True, self.tree.m_expansionRole)

    def on_collapsed(self, index):
        self.tree.model().setData(index, False, self.tree.m_expansionRole)

    def on_currentPageChanged(self, document, page):
        outline=self.outlines.get(document, None)
        if outline:
            found=self.tree.synchronizeOutlineView(page, outline, QModelIndex()) 
            if found.isValid(): self.tree.setCurrentIndex(found)

    def on_viewChanged(self, view):
        document=view.document()
        outline=self.outlines.get(document, None)
        if outline: self.tree.setModel(outline)

    def open(self):
        index=self.tree.currentIndex()
        page=index.data(Qt.UserRole+1)
        left=index.data(Qt.UserRole+2)
        top=index.data(Qt.UserRole+3)

        self.app.window.view().jumpToPage(page, left, top)
        self.app.window.view().setFocus()

    def register(self, document):
        def _run():
            outline=document.loadOutline()
            self.outlines[document]=outline
        t=threading.Thread(target=_run)
        t.daemon=True
        t.start()

    def activate(self, forceShow=False):
        if not self.activated:
            self.activated=True
            self.tree.activate()
        elif self.app.window.view().hasFocus():
            self.tree.setFocus()
        else:
            self.deactivate()

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.tree.deactivate()
