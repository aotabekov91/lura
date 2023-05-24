#!/usr/bin/env python

import os
import sys
import inspect

from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import argparse

from .core import Window
from .modes import Modes
from .utils import Tables
from .utils import Manager

class Lura(QApplication):

    actionRegistered=pyqtSignal()

    def __init__(self):

        super().__init__([])

        self.setConfig()

        self.tables=Tables()
        self.manager=Manager(self)

        self.window=Window(self)
        self.modes=Modes(self)

        self.manager.loadPlugins()
        self.modes.setData()

        self.parse()

    def setConfig(self):

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        self.configPath=f'{mode_path}/config.ini'
        self.config=RawConfigParser()
        self.config.optionxform=str
        self.config.read(self.configPath)

    def parse(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file')
        parser.add_argument('-x', '--xaxis', default=0., type=float)
        parser.add_argument('-y', '--yaxis', default=0., type=float)
        parser.add_argument('-p', '--page', default=0, type=int)
        parser.add_argument('open', nargs='?')
        parsed_args, unparsed_args = parser.parse_known_args()

        if parsed_args.open:
            self.window.open(parsed_args.open)
        view=self.window.display.currentView()
        if view:
            view.jumpToPage(parsed_args.page, parsed_args.xaxis, parsed_args.yaxis)

if __name__ == "__main__":
    app = Lura()
    sys.exit(app.exec_())
