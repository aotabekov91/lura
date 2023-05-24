from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ListWidget(QListWidget):

    def __init__(self, app, parent, location=None, name=None):
        super().__init__(app.window)

        self.app=app
        self.name=name
        self.m_parent=parent
        self.location=location
        self.activated=False

        self.app.window.setTabLocation(self, self.location, self.name)

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.app.window.deactivateTabWidget(self)

    def activate(self):
        self.activated=True
        self.app.window.activateTabWidget(self)
        self.setFocus()
