import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Finder(QObject):

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.window = parent
        self.globalKeys = {
                'Ctrl+p': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.name = 'finder'
        self.setup()

    def setup(self):

        self.fuzzy=self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.actOnFuzzySelection)
        
        self.files=None
        self.path = os.path.abspath('/home/adam/')

    def setFuzzyData(self):
        self.files=[]
        for (_, __, files) in os.walk(self.path):
            for file in files:
                if file.lower().endswith('pdf'):
                    path = os.path.join(_, file)
                    self.files+=[path]
        self.fuzzy.setData(self, self.files)

    def toggle(self):

        if self.files is None:
            self.setFuzzyData()

        self.fuzzy.activate(self)

    def actOnFuzzySelection(self, selected, client):
        if client==self:
            self.fuzzy.deactivate(self)
            self.window.open(selected)

