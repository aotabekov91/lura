import os
import sys
import tomli
import typing as tp

import time

from PyQt6 import QtCore, QtWidgets

import plug

from .. import plugs
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

    appSoonQuits: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appSoonStarts: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appConfigChanged: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appViewIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def setupApp(self):
         self.setupParser()
         self.setupQApp()
         self.setupParts()
         self.setupView()
         self.setupWatcher()

    def setupWatcher(self):
        self.watcher=QtCore.QFileSystemWatcher()
        self.setupConfigWatcher()

    def setupConfigWatcher(self):
        config=self.files.get('config.toml', None)
        if config:
            self.watcher.addPath(config)
            self.watcher.fileChanged.connect(self.resetConfig)
    
    def resetConfig(self, path) -> None:
        n=0
        while not os.path.exists(path):
            time.sleep(0.5)
            n+=1
            if n>5: return
        with open(path, "rb") as y:
            self.m_config = tomli.load(y)
        self.appConfigChanged.emit()
        self.setupConfigWatcher()

    def setupQApp(self) -> None:
         self.qapp: QtWidgets.QApplication = (
             QtWidgets.QApplication(sys.argv)
         )
         self.qapp.setApplicationName(self.name)
         self.setParent(self.qapp)
    
    def setupView(self, klass: tp.Any = View) -> None:
         if klass:
             self.ui = klass(app=self)
    
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

    def activate(self, *args, **kwargs):
        super().activate(*args, **kwargs)
        self.plugman.loadKlasses(plugs.get_base_plugs())

    def run(self) -> None:
         self.appSoonStarts.emit()
         self.startView()
         self.appViewIsLaunched.emit()
         self.running=True
         self.appIsLaunched.emit()
         sys.exit(self.qapp.exec())
