import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from plugin import register

from lura.utils import Plugin
from lura.utils.widgets import BaseCommandStack

from .widget import Tree

class FileBrowser(Plugin):

    def __init__(self, app):

        super().__init__(app)

        self.setUI()

    def setUI(self):
        
        self.ui=BaseCommandStack(self, 'left')
        self.ui.addWidget(Tree(), 'tree', main=True)
        self.ui.tree.openWanted.connect(self.on_openWanted)
        self.ui.hideWanted.connect(self.deactivate)

    def on_openWanted(self, how, focus):

        self.open(how=how, focus=focus)

    def activate(self):

        self.activated=True
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    @register('f', info='File browser', command=True)
    def toggle(self): super().toggle()

    def open(self, how='reset', focus=True):

        if self.ui.tree.currentIndex():
            path=self.ui.tree.model().filePath(self.ui.tree.currentIndex())
            if os.path.isdir(path): 
                self.ui.tree.expand(self.ui.tree.currentIndex())
            else:
                self.app.window.open(path, how=how, focus=focus)
