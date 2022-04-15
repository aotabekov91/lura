import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .tree import TreeFileBrowser


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

        self.m_view = TreeFileBrowser(self, self.s_settings)
        self.m_view.open=self.open

        self.window.plugin.command.addCommands(
            [('fbc - file browser choose path', 'choose')], self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.m_view)

        self.window.setTabLocation(self, self.location, self.name)

    def choose(self):
        self.pathChosen.emit(self.m_view.currentPath())
        self.m_view.setFocus()

    def toggle(self):

        if not self.activated:

            self.window.activateTabWidget(self)
            self.m_view.tree(self.path)
            self.setFocus()
            self.m_view.setFocus()
            self.activated = True

        else:

            self.window.deactivateTabWidget(self)
            self.activated = False

    def open(self):
        self.window.open(self.m_view.currentPath())
