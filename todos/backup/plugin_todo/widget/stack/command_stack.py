from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import StackWidget
from ..compound import CommandList

class CommandStack(StackWidget):

    commandExecuted=pyqtSignal()

    def __init__(self):

        super(CommandStack, self).__init__()
        super().addWidget(CommandList(), 'commands')

        self.commands.commandExecuted.connect(self.commandExecuted)

    def toggleCommands(self):

        if self.current==self.commands:
            if self.previous!=self.commands:
                self.show(self.previous)
            else:
                self.show(self.main)
        else:
            self.show(self.commands)
