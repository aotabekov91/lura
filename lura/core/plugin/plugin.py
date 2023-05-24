#!/usr/bin/python3
import os
import inspect
from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core import Actions
from lura.utils import classify

class Plugin(Actions):

    def __init__(self, app, name=None, widget=None):
        super(Plugin, self).__init__(app, name, widget)
        self.activated=False

    def setConfig(self):
        config=self.readConfig()
        if config.has_section(self.name):
            self.config=config[self.name]
        else:
            self.config=RawConfigParser()
        self.setShortcuts()

    @classify(parent='display', context=Qt.WidgetWithChildrenShortcut)
    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()
    
    def activateStatusbar(self):
        statusbar=self.app.window.statusBar()
        statusbar.setDetailInfo(self.name)
        statusbar.show()

    def deactivateStatusbar(self):
        statusbar=self.app.window.statusBar()
        statusbar.setDetailInfo('')
        statusbar.hide()

    def activate(self, focus=True):
        if not self.activated:
            self.activated=True
            self.activateStatusbar()
            if focus:
                self.show()
                self.setFocus()

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.deactivateStatusbar()
            self.app.window.display.focusCurrentView()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.deactivate()
        else:
            super().keyPressEvent(event)
