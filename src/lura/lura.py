from PyQt5 import QtCore

from qapp.app import BaseApp

from .viewer import LuraView
from .modes import Normal, Command, Visual
from .utils import LuraDisplay, LuraBuffer

class Lura(BaseApp):

    actionRegistered=QtCore.pyqtSignal()

    def setParser(self):

        super().setParser()
        self.parser.add_argument(
                '-p', '--page', default=0, type=int)
        self.parser.add_argument(
                '-x', '--xaxis', default=0., type=float)
        self.parser.add_argument(
                '-y', '--yaxis', default=0., type=float)

    def setStack(self, display_class=None, view_class=None):

        super().setStack(LuraDisplay, LuraView)

    def initiate(self):

        self.manager.setBufferManager(LuraBuffer)
        super().initiate()

    def loadModes(self): 

        for mode_class in [Normal, Command, Visual]: 
            self.modes.addMode(mode_class(self))

        self.modes.setMode('normal')

    def parse(self):

        args, unkw = self.parser.parse_known_args()

        if args.file:
            self.main.open(filePath=args.file)

        if args.page:
            view=self.main.display.currentView()
            if view: 
                view.goto(args.page, args.xaxis, args.yaxis)
