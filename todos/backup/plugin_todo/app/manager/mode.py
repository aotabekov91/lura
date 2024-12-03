from PyQt5.QtCore import *

class Modes(QObject):

    def __init__(self, app):

        super().__init__(app)

        self.app=app
        self.current=None

        self.modes=[]
        self.leaders={}

    def load(self): pass

    def addMode(self, mode):

        mode.setData()
        self.modes+=[mode]
        setattr(self, mode.name, mode) 

        mode.listenWanted.connect(self.setMode)
        mode.delistenWanted.connect(self.setMode)

        if mode.listen_leader: self.leaders[mode.listen_leader]=mode

    def delisten(self):

        for mode in self.modes: mode.listening=False

    def setMode(self, mode_name=None):

        for mode in self.modes: mode.delisten()

        if not mode_name: mode_name='normal'
        current=getattr(self, mode_name, None)

        if current: current.listen()
