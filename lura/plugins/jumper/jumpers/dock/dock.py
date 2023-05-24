from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin

class DockJumper(Plugin):

    def toggleFullSize(self): self.app.window.docks.toggleFullSize()

    def focusLeft(self): self.focus('left')

    def focusTop(self): self.focus('top')

    def focusBottom(self): self.focus('bottom')

    def focusRight(self): self.focus('right')

    def increaseSize(self): self.app.window.docks.resize(1.1)

    def decreaseSize(self): self.app.window.docks.resize(0.9)

    def focus(self, position): self.app.window.docks.focus(position)

    def hideAll(self): self.app.window.docks.hideAll()
