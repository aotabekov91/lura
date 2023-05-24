#!/usr/bin/env python

import os
import sys
import inspect

from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import argparse

from lura.core import Tables
from lura.core import Window
from lura.core import Plugins

class Lura(QApplication):

    def __init__(self):

        super().__init__([])

        self.actions={}
        self.setConfig()

        # Order is important
        self.tables=Tables(self)
        self.window=Window(self)
        self.plugin=Plugins(self)

        self.window.setActions()

        self.parseArgs()

    def setConfig(self):
        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        self.configPath=f'{mode_path}/config.ini'
        self.config=RawConfigParser()
        self.config.optionxform=str
        self.config.read(self.configPath)

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file')
        parser.add_argument('open', nargs='?')
        parsed_args, unparsed_args = parser.parse_known_args()
        if parsed_args.open:
            self.window.open(parsed_args.open)


if __name__ == "__main__":
    app = Lura()
    sys.exit(app.exec_())
