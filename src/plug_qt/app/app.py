import sys
import typing as tp

from PyQt6 import QtCore, QtWidgets

import plug

from . import view
from .earman import Earman
from .buffman import Buffman
from .plugman import Plugman
from .styleman import Styleman
from .stateman import Stateman


class App(
    plug.App,
    QtCore.QObject,
):
    """The main application construct"""

    app_wait: int = 1

    appIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appSoonStarts: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appSoonQuits: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def setup(self) -> None:
         """Setting up the components of the application"""
         super().setup()
         self.setupParser()
         self.setupPool()
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
         view: tp.Any = view.View
     ) -> None:
         if view:
             self.ui = view(app=self)
    
    def setupParts(
         self,
         plugman: tp.Callable[
             [...], tp.Any 
         ] = Plugman,
         earman: tp.Callable[[...], tp.Any] = Earman,
         buffman: tp.Callable[
             [...], tp.Any 
         ] = Buffman,
         styleman: tp.Callable[
             [...], tp.Any 
         ] = Styleman,
         stateman: tp.Callable[
             [...], tp.Any 
         ] = Stateman,
     ) -> None:
         self.earman: Earman = earman(self)
         self.stateman: Stateman = stateman(self)
         self.buffman: Buffman = buffman(self)
         self.plugman: Plugman = plugman(self)
         self.styleman: Styleman = styleman(self)
         # self.earman.add(self.stateman)
         # self.earman.add(self.styleman)
         # self.earman.add(self.buffman)
         # self.earman.add(self.plugman)
         # self.earman.add(self.ui)
         self.earman.add(self.earman)
         self.earman.add(self)
    
    def setupPool(self) -> None:
         self.pool: QtCore.QThreadPool = QtCore.QThreadPool()
    
    def run(self) -> None:
         self.appSoonStarts.emit()
         self.startUI()
         self.appIsLaunched.emit()
         sys.exit(self.qapp.exec())
