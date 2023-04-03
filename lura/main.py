#!/usr/bin/env python

import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import argparse
from configparser import ConfigParser

from lura.utils import WindowManager
from lura.utils import BufferManager
from lura.utils import PluginManager
from lura.utils import TablesManager

class App(QApplication):

    def __init__(self):
        super().__init__([])

        self.set_config()

        self.actions={}

        self.tables=TablesManager(self)
        self.window=WindowManager(self)
        self.buffer=BufferManager(self)
        self.plugin=PluginManager(self)

        self.parse_args()

    def set_config(self):
        main_path=os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        config_path=f'{main_path}/config.ini'
        if os.path.isfile(config_path):
            self.config=ConfigParser()
            self.config.read(config_path)
        else:
            self.config=ConfigParser()

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file')
        parser.add_argument('open', nargs='?')
        parsed_args, unparsed_args = parser.parse_known_args()
        if parsed_args.open:
            self.window.open(parsed_args.open)

if __name__ == "__main__":
    app = App()
    sys.exit(app.exec_())
