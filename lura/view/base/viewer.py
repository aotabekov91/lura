from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class View:

    def readjust(self):
        pass

    def open(self, document):
        pass

    def fitToPageSize(self):
        pass

    def fitToPageWidth(self):
        pass

    def document(self):
        pass

    def close(self):
        pass

    def save(self):
        pass

    def setShortcuts(self):

        if hasattr(self, 'globalKeys'):
            for key, (func, parent, context) in self.globalKeys.items():
                key=QKeySequence(key)
                shortcut=QShortcut(key, parent)
                shortcut.setContext(context)
                shortcut.activated.connect(func)
