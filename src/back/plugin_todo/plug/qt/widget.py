import os
import inspect
from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import PlugQT

class PlugWidget(PlugQT, QWidget):

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()
    
    def activate(self, focus=True):

        if not self.activated:
            self.activated=True
            self.show()
            self.setFocus()

    def deactivate(self):

        if self.activated:
            self.activated=False
            self.hide()

    def keyPressEvent(self, event):

        if event.key()==Qt.Key_Escape:
            self.deactivate()
        else:
            super().keyPressEvent(event)
