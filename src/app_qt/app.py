import os
import sys
import time
import pathlib
import typing as tp

from PyQt6 import QtCore, QtWidgets

from plug import Plug
from gizmo import utils

from . import components, view


class App(
    Plug,
    QtCore.QObject,
):
    """The main application construct"""

    app_wait: int = 2
    canHide: bool = False
    waiting_to_finish: int = 0
    appIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appSoonQuits: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def setup(self) -> None:
         """Setting up the components of the application"""
         super().setup()
         self.setupParser()
         self.setupTools()
         self.setupTimer()
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
         ] = components.Plugman,
         earman: tp.Callable[[...], tp.Any] = components.Earman,
         buffman: tp.Callable[
             [...], tp.Any 
         ] = components.Buffman,
         styleman: tp.Callable[
             [...], tp.Any 
         ] = components.Styleman,
         stateman: tp.Callable[
             [...], tp.Any 
         ] = components.Stateman,
     ) -> None:
         self.earman: components.Earman = earman(self)
         self.stateman: components.Stateman = stateman(self)
         self.buffman: components.Buffman = buffman(self)
         self.plugman: components.Plugman = plugman(self)
         self.styleman: components.Styleman = styleman(self)
         # self.earman.add(self.stateman)
         # self.earman.add(self.styleman)
         # self.earman.add(self.buffman)
         # self.earman.add(self.plugman)
         # self.earman.add(self.ui)
         self.earman.add(self.earman)
         self.earman.add(self)
    
    def setupPool(self) -> None:
         self.pool: QtCore.QThreadPool = QtCore.QThreadPool()
    
    def setupTimer(self):
         self.timer: QtCore.QTimer = QtCore.QTimer()
         self.timer.timeout.connect(self.appIsLaunched.emit)
         self.timer.setSingleShot(True)
    
    def setupParser(self, parser=utils.Parser):
         if parser:
             self.parser: tp.Any = parser()
    
    def setupTools(self, tools=utils.dotdict):
         if tools:
             self.tools: tp.Any = tools()
    
    def activate(self):
         self.plugman.load()
         if self.ui:
             self.ui.show()
    
    def createFolder(
         self,
         path: str = None,
         parents: bool = True,
         exist_ok: bool = True,
     ) -> pathlib.Path:
         path = path or f"~/{self.name.lower()}"
         f = os.path.expanduser(path)
         path = pathlib.Path(f)
         if not os.path.exists(f):
             path.mkdir(parents=parents, exist_ok=exist_ok)
         return path
    
    def wait(self, delta: int) -> None:
         self.waiting_to_finish += delta
    
    def run(self) -> None:
         if self.ui:
             self.ui.activate()
         self.timer.start(self.app_wait)
         sys.exit(self.qapp.exec())
    
    @utils.tag(["<c-q>(any)", "q(normal)"])
    def quit(self) -> None:
         self.appSoonQuits.emit()
         time.sleep(0.1)
         while self.waiting_to_finish:
             time.sleep(0.01)
         self.pool.clear()
         sys.exit()
    
    @utils.tag("<c-[>(normal)")
    def hide(self) -> None:
         if self.ui and self.canHide:
             self.ui.hide()
    
    def standardEvent(self, event):
         return event
