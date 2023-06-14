from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.widget import InputListStack, CommandStack, ListWidget

class Base:

    def __init__(self, plugin, location, *args, **kwargs):

        super(Base, self).__init__(*args, **kwargs)

        self.plugin=plugin
        self.app=plugin.app
        self.activated=False

        self.app.main.docks.setTab(self, location)

    def deactivate(self): 

        if self.activated:

            self.activated=False
            self.plugin.actOnDefocus()
            self.dock.deactivate(self)

    def activate(self): 

        self.activated=True
        self.plugin.actOnFocus()
        self.dock.activate(self)

class BaseListWidget(Base, ListWidget): pass

class BaseCommandStack(Base, CommandStack): pass

class BaseInputListStack(Base, InputListStack): pass
