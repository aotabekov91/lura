from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import sys
import inspect
import functools

from configparser import RawConfigParser

from lura.utils import classify

class Actions(QWidget):

    def __init__(self, app, name=None, widget=None): 
        super(Actions, self).__init__(app.window)
        self.app=app
        self.name=name
        self.widget=widget
        self.setName()
        self.setConfig()

    def setName(self):
        if self.name is None: 
            self.name=self.__class__.__name__
        if self.widget is None:
            self.widget=self

    def setConfig(self):
        if self.app.config.has_section(self.name):
            self.config=self.app.config[self.name]
        else:
            self.config=RawConfigParser()
        if hasattr(self.widget, 'setSettings'):
            self.widget.setSettings(self.config)
        self.setShortcuts()

    def readConfig(self, configs=[]):
        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        config_path=f'{mode_path}/config.ini'
        config=RawConfigParser()
        config.optionxform=str
        configs+=[config_path]
        config.read(configs)
        return config

    def setShortcuts(self):
        config={}
        if self.app.config.has_section(self.name):
            config=dict(self.app.config[self.name])
        config.update(dict(self.config.items()))
        for func_name, key in config.items():
            func=getattr(self.widget, func_name, None)
            if func and hasattr(func, 'parent'): 
                if func.parent=='window':
                    widget=self.app.window
                elif func.parent=='display':
                    widget=self.app.window.display
                elif func.parent=='own':
                    if self.widget:
                        widget=self.widget
                    else:
                        widget=self
                else:
                    widget=self
                    elements=func.parent.split('.')
                    if elements:
                        for e in elements:
                            widget=getattr(widget, e, None)
                context=getattr(func, 'context', Qt.WidgetWithChildrenShortcut)
                shortcut=QShortcut(widget)
                shortcut.setKey(key)
                shortcut.setContext(context)
                shortcut.activated.connect(func)
                self.app.actions[f'{self.name}_{func_name}']=func

    @classify(parent='own', context=Qt.WindowShortcut)
    def activate(self):
        if not self.widget.hasFocus():
            self.widget.show()
            self.widget.setFocus()
