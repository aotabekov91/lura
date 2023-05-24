import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin, register
from lura.utils import watch, BaseCommandStack

from .widget import OutlineTree

class Outline(Plugin):
    
    def __init__(self, app):

        super().__init__(app, key='o')

        self.outlines={}

        self.app.window.buffer.documentCreated.connect(self.registerDocument)
        self.app.window.display.viewChanged.connect(self.on_viewChanged)
        self.app.window.display.currentPageChanged.connect(self.on_currentPageChanged)

        self.setUI()

    def setUI(self):

        self.ui=BaseCommandStack(self, 'left')
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
            self.app.window.display.currentView().jumpToPage(page, left, top)

    def on_outlineExpanded(self, index):

        self.ui.tree.model().setData(index, True, self.ui.tree.m_expansionRole)

    def on_outlineCollapsed(self, index):

        self.ui.tree.model().setData(index, False, self.ui.tree.m_expansionRole)

    def on_currentPageChanged(self, document, currentPage, prevPage):

        outline=self.outlines.get(document, None)
        if outline:
            index=self.ui.tree.currentIndex()
            found=self.ui.tree.synchronizeOutlineView(currentPage, outline, QModelIndex()) 
            if found.isValid(): self.ui.tree.setCurrentIndex(found)

    def on_viewChanged(self, view):

        document=view.document()
        outline=self.outlines.get(document, None)
        if outline: self.ui.tree.setModel(outline)

    @register('t')
    def toggle(self): super().toggle()

    @register('o')
    def open(self):

        if self.activated:

            index=self.ui.tree.currentIndex()
            page=index.data(Qt.UserRole+1)
            left=index.data(Qt.UserRole+2)
            top=index.data(Qt.UserRole+3)
            self.app.window.display.currentView().jumpToPage(page, left, top)
            self.app.window.display.currentView().setFocus()

    def registerDocument(self, document):

        def _run():

            outline=document.loadOutline()
            self.outlines[document]=outline
        t=threading.Thread(target=_run)
        t.daemon=True
        t.start()

    @register('a')
    def activate(self):

        self.activated=True
        self.ui.activate()

    @register('d')
    def deactivate(self):

        self.activated=False
        self.ui.deactivate()
