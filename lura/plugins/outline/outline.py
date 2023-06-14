import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin, register
from lura.utils import watch, BaseCommandStack

from .widget import OutlineTree

class Outline(Plugin):
    
    def __init__(self, app):

        super().__init__(app, position='left', mode_keys={'command': 'o'})

        self.setUI()

    def setUI(self):

        super().setUI()

        self.ui.addWidget(OutlineTree(), 'tree', main=True)

        self.ui.tree.clicked.connect(self.on_outlineClicked)
        self.ui.tree.expanded.connect(self.on_outlineExpanded)
        self.ui.tree.collapsed.connect(self.on_outlineCollapsed)
        self.ui.tree.returnPressed.connect(self.on_outlineClicked)
        self.ui.tree.openWanted.connect(self.on_outlineClicked)
        self.ui.tree.hideWanted.connect(self.deactivate)

        self.ui.installEventFilter(self)

    def on_outlineClicked(self, index=None):

        if index is None: index=self.ui.tree.currentIndex()
        if index:
            page=index.data(Qt.UserRole+1)
            left=index.data(Qt.UserRole+2)
            top=index.data(Qt.UserRole+3)
            self.app.main.display.currentView().jumpToPage(page, left, top)

    def on_outlineExpanded(self, index):

        self.ui.tree.model().setData(index, True, self.ui.tree.m_expansionRole)

    def on_outlineCollapsed(self, index):

        self.ui.tree.model().setData(index, False, self.ui.tree.m_expansionRole)

    def on_currentPageChanged(self, document, currentPage, prevPage):

        if self.outline:
            index=self.ui.tree.currentIndex()
            found=self.ui.tree.synchronizeOutlineView(currentPage, self.outline, QModelIndex()) 
            if found.isValid(): self.ui.tree.setCurrentIndex(found)

    def on_viewChanged(self, view):

        self.setData()
        if self.outline: self.ui.tree.setModel(self.outline)

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    @register('o')
    def open(self):

        if self.activated:

            index=self.ui.tree.currentIndex()
            page=index.data(Qt.UserRole+1)
            left=index.data(Qt.UserRole+2)
            top=index.data(Qt.UserRole+3)
            self.app.main.display.currentView().jumpToPage(page, left, top)
            self.app.main.display.currentView().setFocus()

    def setData(self):

        self.outline=None

        view=self.app.main.display.view
        if view:
            document=view.document()
            self.outline=document.loadOutline()

    def activate(self):

        self.activated=True

        self.setData()
        self.ui.activate()

        self.app.main.display.viewChanged.connect(self.on_viewChanged)
        self.app.main.display.currentPageChanged.connect(self.on_currentPageChanged)

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

        self.app.main.display.viewChanged.disconnect(self.on_viewChanged)
        self.app.main.display.currentPageChanged.disconnect(self.on_currentPageChanged)
