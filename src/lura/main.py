from PyQt5 import QtCore

from qapp.plug import PlugApp

from .viewer import LuraView
from .modes import Normal, Command, Visual
from .utils import LuraDisplay, LuraBuffer

class Lura(PlugApp):

    actionRegistered=QtCore.pyqtSignal()

    def __init__(self): super().__init__(initiate_stack=True)

    def setParser(self):

        super().setParser()

        self.parser.add_argument(
                'file', nargs='?', default=None, type=str)
        self.parser.add_argument(
                '-p', '--page', default=0, type=int)
        self.parser.add_argument(
                '-x', '--xaxis', default=0., type=float)
        self.parser.add_argument(
                '-y', '--yaxis', default=0., type=float)

    def setStack(self): super().setStack(LuraDisplay, LuraView)

    def setManager(self): super().setManager(buffer=LuraBuffer)

    def loadModes(self): 

        for m in [Normal, Command, Visual]: 
            self.modes.addMode(m(self))
        self.modes.setMode('normal')

    def parse(self):

        args, unkw = super().parse()

        if args.file:
            self.main.open(filePath=args.file)

        if args.page:
            view=self.main.display.currentView()
            if view: 
                view.goto(args.page, args.xaxis, args.yaxis)

def run():

    app=Lura()
    app.run()
