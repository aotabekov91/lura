from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.widget import InputListEditStack

class InputListEdit(InputListEditStack):

    def __init__(self, app, parent, location, name):
        super(InputListEdit, self).__init__()

        self.app=app
        self.name=name
        self.m_parent=parent
        self.location=location
        self.app.window.docks.setTabLocation(self, self.location, self.name)

    def deactivate(self):
        self.app.window.docks.deactivateTabWidget(self)

    def activate(self):
        self.app.window.docks.activateTabWidget(self)
        self.adjustSize()
        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Q, Qt.Key_Escape]:
            self.m_parent.deactivate()
        else:
            super().keyPressEvent(event)
