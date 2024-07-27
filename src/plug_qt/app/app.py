import sys
import typing as tp

from PyQt6 import QtCore, QtWidgets

import plug

from .view import View
from .earman import Earman
from .buffman import Buffman
from .plugman import Plugman
from .styleman import Styleman
from .stateman import Stateman


class App(
    plug.App,
    QtCore.QObject,
):

    app_wait: int = 1
    appSoonQuits: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appSoonStarts: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def setupApp(self):
         self.setupParser()
         self.setupQApp()
         self.setupParts()
         self.setupView()
    
    def setupQApp(self) -> None:
         self.qapp: QtWidgets.QApplication = (
             QtWidgets.QApplication(sys.argv)
         )
         self.qapp.setApplicationName(self.name)
         self.setParent(self.qapp)
    
    def setupView(
         self, 
         view: tp.Any = View
     ) -> None:
         if view:
             self.ui = view(app=self)
    
    def setupParts(
         self,
         plugman = Plugman,
         earman = Earman,
         buffman = Buffman,
         styleman = Styleman,
         stateman = Stateman,
     ) -> None:
         super().setupParts(
                 plugman=plugman,
                 earman=earman,
                 buffman=buffman,
                 styleman=styleman,
                 stateman=stateman)

    def run(self) -> None:
         self.appSoonStarts.emit()
         self.startUI()
         self.running=True
         self.appIsLaunched.emit()
         sys.exit(self.qapp.exec())
