#!/usr/bin/python3
import os
import inspect
from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Plugin(QObject):

    def __init__(self, app, name=None):
        super(Plugin, self).__init__(app.window)
        self.app=app
        self.name = name 
        self.activated=False
        self.shortcuts={}
        self.localcuts={}
        self.actions={}
        self.set_config()
        self.set_shortcuts()
        self.set_localcuts()

    def activate(self):
        self.activated=True

    def set_config(self):

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        config_path=f'{mode_path}/config.ini'
        if os.path.isfile(config_path):
            self.config=RawConfigParser()
            self.config.optionxform=str
            self.config.read(config_path)
        else:
            self.config=RawConfigParser()

        if self.config.has_section('Shortcuts'):
            self.shortcuts=dict(self.config.items('Shortcuts'))
        if self.config.has_section('Localcuts'):
            self.localcuts=dict(self.config.items('Localcuts'))

    def set_localcuts(self):
        for func_name, key in self.localcuts.items():
            func=getattr(self, func_name, None)
            if func: self.actions[key]=func

    def set_shortcuts(self, level='window', parent_widget='display'):

        if level=='widget_with_children':
            context=Qt.WidgetWithChildrenShortcut
        elif level=='window':
            context=Qt.WindowShortcut
        else:
            raise

        if parent_widget=='display':
            widget=self.app.window.display
        elif parent_widget=='window':
            widget=self.app.window
        else:
            raise

        for func_name, key in self.shortcuts.items():
            func=getattr(self, func_name, None)
            if func: 
                shortcut=QShortcut(QKeySequence(str(key)), widget, context=context)
                shortcut.activated.connect(func)
