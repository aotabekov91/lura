#!/usr/bin/python3
import os
import inspect
from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Plugin(QWidget):

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

        self.app.window.mouseReleaseEventOccured.connect(self.on_mouseReleaseEvent)

    def on_mouseReleaseEvent(self, event, pageItem, view):
        if self.activated: self.setFocus()

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

    def set_localcuts(self, widget=None):
        if not widget: widget=self
        for func_name, key in self.localcuts.items():
            func=getattr(self, func_name, None)
            if func:
                self.actions[key]=func
                context=Qt.WidgetWithChildrenShortcut
                shortcut=QShortcut(widget)
                shortcut.setKey(key)
                shortcut.setContext(context)
                shortcut.activated.connect(func)

    def set_shortcuts(self, parent_widget='display'):
        if parent_widget=='display':
            widget=self.app.window.display
            context=Qt.WidgetWithChildrenShortcut
        elif parent_widget=='window':
            widget=self.app.window
            context=Qt.WindowShortcut
        else:
            raise

        for func_name, key in self.shortcuts.items():
            func=getattr(self, func_name, None)
            if func: 
                shortcut=QShortcut(widget)
                shortcut.setKey(key)
                shortcut.setContext(context)
                shortcut.activated.connect(func)

    def activate(self):
        if not self.activated:
            self.activated=True
            statusbar=self.app.window.statusBar()
            statusbar.setDetailInfo(self.name)
            statusbar.show()
            self.show()
            self.setFocus()
        else:
            self.deactivate()

    def deactivate(self):
        self.activated=False
        statusbar=self.app.window.statusBar()
        statusbar.setDetailInfo('')
        statusbar.hide()
        view=self.app.window.view()
        if view:
            view.setFocus()
        else:
            sef.app.window.setFocus()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.deactivate()
        else:
            super().keyPressEvent(event)
