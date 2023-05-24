from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.widget import InputList
from plugin.widget import UpDownEdit
from plugin.widget import Stack

class ListWidget (Stack):

    contentUpdateOccurred=pyqtSignal(int, str)
    keyPressEventOccurred=pyqtSignal(object)
    listReturnPressed=pyqtSignal()
    inputReturnPressed=pyqtSignal()

    def __init__(self, app, parent, location=None, name=''):
        super(ListWidget, self).__init__()

        self.app=app
        self.name=name
        self.m_parent=parent
        self.location=location
        self.app.window.docks.setTabLocation(self, self.location, self.name)
        self.setUI()

    def setUI(self):

        self.list=InputList(widget_class=UpDownEdit)
        self.setMainWidget(self.list)

    def setList(self, dlist):
        self.list.setList(dlist)

    def focusList(self):
        pass

    def focusInput(self):
        pass

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
