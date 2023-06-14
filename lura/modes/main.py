from PyQt5.QtCore import *

from .visual import Visual
from .normal import Normal
from .command import Command

from lura.utils import register

class Modes(QObject):

    def __init__(self, app):

        super().__init__(app)

        self.app=app
        self.current=None

        self.modes=[]
        self.leaders={}

    def addModes(self):

        self.normal=Normal(self.app)
        self.visual=Visual(self.app)
        self.command=Command(self.app)

        self.setMode('normal')

        # self.app.main.bar.hideWanted.connect(self.setMode)

    def addMode(self, mode):

        self.modes+=[mode]
        mode.setData()

        mode.listenWanted.connect(self.setMode)
        mode.delistenWanted.connect(self.setMode)

        if mode.listen_leader: self.leaders[mode.listen_leader]=mode

        setattr(self, mode.name, mode) 

    def delisten(self):

        for mode in self.modes: mode.listening=False

    def setMode(self, mode_name=None):

        for mode in self.modes: mode.delisten()

        if not mode_name: mode_name='normal'
        current=getattr(self, mode_name, None)

        if current: current.listen()
