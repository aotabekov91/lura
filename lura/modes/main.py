from PyQt5.QtCore import *

from .plug import Plug
from .focus import Focus
from .normal import Normal
from .command import Command

from .visual import Visual

from lura.utils import register

class Modes(QObject):

    def __init__(self, app):

        super().__init__(app)

        self.app=app
        self.modes=[]
        self.current=None

        self.addMode(Plug)
        self.addMode(Normal)
        self.addMode(Focus)
        self.addMode(Command)
        self.addMode(Visual)

        self.setMode('normal')

        self.app.window.bar.hideWanted.connect(self.setMode)

    def addMode(self, mode_class):

        mode=mode_class(self.app)

        mode.listenWanted.connect(self.setMode)
        mode.delistenWanted.connect(self.setMode)

        self.modes+=[mode]
        setattr(self, mode.name, mode) 

    def setData(self):

        for mode in self.modes: mode.setData()

    def delisten(self, mode_name=None):

        if not mode_name:
            for mode in self.modes: 
                mode.listening=False
        else:
            mode=getattr(self, mode_name)
            mode.listening=False

    def listen(self, mode_name):

        self.delisten()
        mode=getattr(self, mode_name)
        mode.listening=True
        self.current=mode

    def setMode(self, mode_name=None):

        if not mode_name: mode_name='normal'

        for mode in self.modes: 
            if mode.name!=mode_name: 
                mode.delisten(force=True)

        self.current=getattr(self, mode_name)
        self.current.listen()
