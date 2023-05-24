from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import InputListStack, CommandStack, register

class Base:

    def __init__(self, plugin, location, *args, **kwargs):

        super(Base, self).__init__(*args, **kwargs)

        self.plugin=plugin
        self.app=plugin.app

        self.app.window.docks.setTab(self, location)

    def deactivate(self): 

        self.activated=False
        self.dock.deactivate(self)

        self.plugin.deactivateCommandMode()
        self.app.window.display.focusCurrentView()

    def activate(self): 

        self.activated=True
        self.dock.activate(self)

class BaseCommandStack(Base, CommandStack): pass

class BaseInputListStack(Base, InputListStack): pass
