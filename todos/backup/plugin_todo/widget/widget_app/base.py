from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import ListWidget
from ..stack import InputListStack, CommandStack

class BaseAppWidget:

    def __init__(self, plugin, location, *args, **kwargs):

        self.name=None
        self.kind=None
        self.activated=False

        super(BaseAppWidget, self).__init__(*args, **kwargs)

        self.plugin=plugin
        self.app=plugin.app
        self.location=location

        if not self.name: 
            self.name=self.plugin.__class__.__name__

        self.locate()

    def locate(self):

        if not self.location or self.location=='window':
            self.kind='window'
            self.app.stack.add(self, self.name) 
        else:
            self.kind='dock'
            self.app.main.docks.setTab(self, self.location)

    def delocate(self):

        if self.kind=='window':
            self.app.stack.remove(self)
        if self.kind=='dock':
            self.app.main.docks.delTab(self)

    def relocate(self, location):

        self.delocate()
        self.location=location
        self.locate()
        self.activate()

    def deactivate(self): 

        if self.activated:

            self.activated=False
            self.plugin.actOnDefocus()

            if self.kind=='dock':
                self.dock.deactivate(self)
            elif self.kind=='window':
                self.app.stack.show(self.app.main)

    def activate(self, force=True): 

        if not self.activated or force:

            self.activated=True
            self.plugin.actOnFocus()

            if self.kind=='dock':
                self.dock.activate(self)
            elif self.kind=='window':
                self.app.stack.show(self)

class BaseListWidget(BaseAppWidget, ListWidget): pass

class BaseCommandStack(BaseAppWidget, CommandStack): pass

class BaseInputListStack(BaseAppWidget, InputListStack): pass
