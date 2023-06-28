import argparse

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tables import Tables
from tables import Metadata, Hash, Annotation

from plugin.app import BaseApp

from .modes import *
from .viewer import LuraView
from .utils import LuraDisplay, LuraBuffer

class Lura(BaseApp):

    actionRegistered=pyqtSignal()

    def __init__(self):

        self.loadTables()
        super().__init__()

    def setStack(self, display_class=None, view_class=None):

        super().setStack(LuraDisplay, LuraView)

    def loadTables(self):

        self.tables=Tables()
        self.tables.add_table(Hash, 'hash')
        self.tables.add_table(Metadata, 'metadata')
        self.tables.add_table(Annotation, 'annotation') 

    def parse(self):

        parser = argparse.ArgumentParser()

        parser.add_argument('file', nargs='?', default=None, type=str)
        parser.add_argument('-p', '--page', default=0, type=int)
        parser.add_argument('-x', '--xaxis', default=0., type=float)
        parser.add_argument('-y', '--yaxis', default=0., type=float)

        parsed_args, unparsed_args = parser.parse_known_args()

        if parsed_args.file:
            self.main.open(filePath=parsed_args.file)

        if parsed_args.page:
            view=self.main.display.currentView()
            if view: 
                view.goto(
                        parsed_args.page, 
                        parsed_args.xaxis, 
                        parsed_args.yaxis)

    def initiate(self):

        self.manager.setBufferManager(LuraBuffer)
        super().initiate()

    def loadModes(self): 

        for mode_class in [Normal, Command, Visual]: 

            mode=mode_class(self)
            self.modes.addMode(mode)

        self.modes.setMode('normal')

if __name__ == "__main__":
    app = Lura()
    sys.exit(app.exec_())
