from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.widgets.tree import Item
from lura.core.widgets.tree import TreeView

from lura.render.map import BaseMapDocument 

from lura.core.widgets.tree.menus import ChangeMenu
from lura.core.widgets.tree.menus import ToggleMenu

class Display(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.s_settings=settings
        self.location='right'
        self.name='Annotations'
        self.setup()

    def resizeEvent(self, event):
        self.m_view.setFixedWidth()

    def setup(self):

        self.activated=False

        self.m_view=TreeView(self)
        self.m_model=BaseMapDocument()
        self.m_view.setModel(self.m_model)

        layout=QVBoxLayout(self)

        self.m_changeMenu=ChangeMenu(self)
        self.m_toggleMenu=ToggleMenu(self)

        layout.addWidget(self.m_view)
        layout.addWidget(self.m_changeMenu)
        layout.addWidget(self.m_toggleMenu)

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.setTabLocation(self, self.location, self.name)

        self.setActions()

    def setActions(self):
        self.actions=[]
        for func, key in self.s_settings['shortcuts'].items():

            m_action=QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
            self.actions+=[m_action]
            m_action.triggered.connect(getattr(self, func))
            self.addAction(m_action)

    def toggleToggleMenu(self):
        self.hideMenus()
        self.m_toggleMenu.toggle()

    def toggleChangeMenu(self):
        self.hideMenus()
        self.m_changeMenu.toggle()

    def open(self):
        item=self.m_view.currentItem()
        if item is None: return
        if item.itemData().kind()=='annotation':
            pageNumber=item.itemData().page().pageNumber()
            document=item.itemData().page().document()
            self.window.view().open(document)
            self.window.view().jumpToPage(pageNumber)

    def hideMenus(self):
        self.m_toggleMenu.hide()
        self.m_changeMenu.hide()
        self.m_view.setFocus()

    def on_viewChanged(self, view):
        if not view.document().__class__.__name__ in ['PdfDocument', 'WebDocument']: return
        if not view.document().registered(): return
        self.m_model.clear()
        item=Item(self.window.document())
        self.m_model.appendRow(item)

        for annotation in self.window.document().annotations():
            item.appendRow(Item(annotation))

    def toggle(self):

        if self.window.view() is None: return

        if not self.activated:

            self.window.activateTabWidget(self)
            self.m_view.setFocus()
            self.activated=True

        else:

            self.window.deactivateTabWidget(self)
            self.window.view().setFocus()
            self.activated=False
