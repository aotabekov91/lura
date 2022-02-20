from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core.widgets.miscel import CustomQTreeView

class Outline(CustomQTreeView):
    
    def __init__(self, parent, settings):
        # super().__init__(Qt.UserRole+4, Qt.UserRole+5, parent)
        super().__init__(parent)
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
        self.activated=False

        self.shortcuts={v:k for k,v in self.s_settings['shortcuts'].items()}

        self.m_expansionRole=Qt.UserRole+4
        self.m_expansionIDRole=Qt.UserRole+5

        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.window.setTabLocation(self, 'left', 'Outline')

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.documentRegistered.connect(self.register)
        self.window.currentPageChanged.connect(self.on_currentPageChanged)

        self.expanded.connect(self.on_expanded)
        self.collapsed.connect(self.on_collapsed)

        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.clicked.connect(self.on_outline_clicked)

    def on_outline_clicked(self, index):

        page=index.data(Qt.UserRole+1)
        left=index.data(Qt.UserRole+2)
        top=index.data(Qt.UserRole+3)

        self.window.view.jumpToPage(page, left, top)

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

        outline=self.outlines[document]

        if outline is not None:

            match=self.synchronizeOutlineView(page, outline, QModelIndex()) 

            if match.isValid():
                self.collapseAll()
                self.expandAbove(match)
                self.setCurrentIndex(match)

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

        if not self.activated or forceShow:

            document=self.window.view.m_document
            outline=self.outlines[document]
            self.setModel(outline)

            self.window.activateTabWidget(self)

            self.setFocus()
            self.activated=True

        else:

            self.window.deactivateTabWidget(self)
            self.activated=False

    def on_viewChanged(self, view):
        if not self.activated: return
        self.activated=not self.activated
        self.toggle()

    def open(self):
        index=self.currentIndex()

        page=index.data(Qt.UserRole+1)
        left=index.data(Qt.UserRole+2)
        top=index.data(Qt.UserRole+3)

        self.window.view.jumpToPage(page, left, top)

    def register(self, document):
        outline=document.loadOutline()
        outline.setHorizontalHeaderLabels(['Content', 'Page'])
        self.outlines[document]=outline

    def keyPressEvent(self, event):
        key=event.text()

        if event.key()==Qt.Key_Escape:
            self.toggle()

        elif key in self.shortcuts:
            func=getattr(self, self.shortcuts[key])
            func()

        else:
            super().keyPressEvent(event)


