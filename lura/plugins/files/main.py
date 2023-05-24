import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin, register
from lura.utils.widgets import BaseCommandStack

from .widget import Tree

class FileBrowser(Plugin):

    def __init__(self, app):

        super().__init__(app, position='left', mode_keys={'command': 'f'})

        self.setUI()

    def setUI(self):
        
        super().setUI()

        self.ui.addWidget(Tree(), 'main', main=True)
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('a')
    def activate(self):

        self.activated=True
        self.app.modes.plug.setClient(self)
        self.app.modes.setMode('plug')
        self.ui.activate()

    @register('d')
    def deactivate(self):

        self.activated=False
        self.app.modes.setMode('normal')
        self.ui.deactivate()

    @register('t')
    def toggle(self): super().toggle()

    @register('i')
    def openBelow(self): 

        self.open(how='below', focus=False)
        self.ui.show()

    @register('I')
    def openBelowFocus(self): 

        self.open(how='below', focus=True)

    @register('o')
    def openReset(self): 

        self.open(how='reset', focus=False)

    @register('O')
    def openResetFocus(self): self.open(how='reset', focus=True)
    
    @register('O')
    def openFocus(self): self.open(how='reset', focus=True)

    @register('h')
    def openAndDeactivate(self): 

        self.open(how='reset', focus=True)
        self.deactivate()

    def open(self, how='reset', focus=True):

        if self.ui.main.tree.currentIndex():
            path=self.ui.main.tree.model().filePath(self.ui.main.tree.currentIndex())
            if os.path.isdir(path): 
                self.ui.main.tree.expand(self.ui.main.tree.currentIndex())
            else:
                self.app.window.open(path, how=how, focus=focus)

        if focus:
            self.app.modes.setMode('normal')
            self.app.window.setFocus()
        else:
            self.ui.show()
