import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core import MapTree

class FileBrowser(QWidget):

    pathChosen = pyqtSignal(object)

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings = settings
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

        # self.m_view = TreeFileBrowser(self, self.s_settings)
        self.m_view = MapTree(self)
        self.m_view.open=self.open
        self.setModel()


        self.window.plugin.command.addCommands(
            [('fbc - file browser choose path', 'choose')], self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.m_view)

        self.window.setTabLocation(self, self.location, self.name)

    def choose(self):
        self.pathChosen.emit(self.currentPath())
        self.m_view.setFocus()

    def toggle(self):

        if not self.activated:

            self.window.activateTabWidget(self)
            self.tree(self.path)
            self.setFocus()
            self.m_view.setFocus()
            self.activated = True

        else:

            self.window.deactivateTabWidget(self)
            self.activated = False

    def open(self):
        self.window.open(self.currentPath())

    def tree(self, path=None):

        if path is None: path = os.path.abspath('.')

        self.m_view.model().setRootPath(path)
        self.m_view.setRootIndex(self.m_view.model().index(path))
        self.m_view.setFocus()

    def currentPath(self):
        if self.m_view.currentIndex() is None: return
        return self.m_view.model().filePath(self.currentIndex())

    def setModel(self):
        self.m_view.setModel(QFileSystemModel())
        self.m_view.header().hide()
        for i in range(1, 4):
            self.m_view.hideColumn(i)
