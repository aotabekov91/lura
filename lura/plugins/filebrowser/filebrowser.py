import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .tree import TreeFileBrowser
from lura.core.widgets import Menu

class FileBrowser(QWidget):

    pathChosen=pyqtSignal(object)

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings=settings
        self.location = 'left'
        self.name = 'fileBrowser'

        self.globalKeys = {
                'Ctrl+f': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.activated = False
        self.path = os.path.abspath('.')

        self.m_view=TreeFileBrowser(self, self.s_settings)
        mapping={getattr(self, f):v for f, v in self.s_settings['Menu'].items()}
        self.m_menu=Menu(self, mapping) 
        self.m_menu.setHeight(200)

        layout=QVBoxLayout(self)
        layout.addWidget(self.m_view)
        layout.addWidget(self.m_menu)

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
    
    def choose(self):
        self.m_menu.hide()
        self.pathChosen.emit(self.m_view.currentPath())
        self.m_view.setFocus()

    def makeRoot(self):
        self.m_menu.hide()
        self.m_view.makeRoot()

    def rootUp(self):
        self.m_menu.hide()
        self.m_view.rootUp()

    def toggleMenu(self):
        if self.m_menu.isVisible():
            self.m_menu.hide()
        else:
            self.m_menu.show()
            self.m_menu.setFocus()

    def toggle(self):

        if not self.activated:

            self.window.activateTabWidget(self)
            self.m_view.tree(self.path)
            self.setFocus()
            self.m_view.setFocus()

            self.activated=True

        else:

            self.window.deactivateTabWidget(self)

            self.activated = False
