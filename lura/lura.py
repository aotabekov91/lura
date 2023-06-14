#!/usr/bin/env python

import os
import sys
import inspect

from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import argparse

from .modes import Modes
from .utils import Tables
from .utils import Manager

from .core import StackWindow

class Lura(QApplication):

    actionRegistered=pyqtSignal()

    def __init__(self):

        super().__init__([])

        self.setConfig()

        self.tables=Tables()
        self.modes=Modes(self)
        self.manager=Manager(self)

        self.stack=StackWindow(self)

        self.parse()

        self.manager.loadPlugins()
        self.modes.addModes()

    def setConfig(self):

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        self.configPath=f'{mode_path}/config.ini'
        self.config=RawConfigParser()
        self.config.optionxform=str
        self.config.read(self.configPath)

    def parse(self):

        parser = argparse.ArgumentParser()

        parser.add_argument('-a', '--aid', default=None, type=int)
        parser.add_argument('-b', '--bid', default=None, type=int)
        parser.add_argument('-d', '--dhash', default=None, type=str)

        parser.add_argument('file', nargs='?', default=None, type=str)
        parser.add_argument('-p', '--page', default=0, type=int)
        parser.add_argument('-x', '--xaxis', default=0., type=float)
        parser.add_argument('-y', '--yaxis', default=0., type=float)

        parsed_args, unparsed_args = parser.parse_known_args()

        if parsed_args.file:
            self.main.open(filePath=parsed_args.file)
        elif parsed_args.dhash:
            self.main.openBy(kind='hash', criteria=parsed_args.dhash)
        elif parsed_args.aid:
            self.main.openBy(kind='annotation', criteria=parsed_args.aid)
        elif parsed_args.bid:
            self.main.openBy(kind='bookmark', criteria=parsed_args.bid)

        if parsed_args.page:
            view=self.main.display.currentView()
            if view: view.jumpToPage(parsed_args.page, parsed_args.xaxis, parsed_args.yaxis)

if __name__ == "__main__":
    app = Lura()
    sys.exit(app.exec_())
