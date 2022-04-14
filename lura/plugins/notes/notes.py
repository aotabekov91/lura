from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .display import Display
from .connect import DatabaseConnector

class Notes(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.display=Display(self, settings)
        self.baseFolder=settings['baseFolder']
        self.name = 'notes'
        self.globalKeys={
                'Ctrl+n': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut),
                'Ctrl+Shift+n': (
                    self.display.open,
                    self.window,
                    Qt.WindowShortcut),
                    }
        self.setup()

    def setup(self):
        self.db = DatabaseConnector(self, self.window)

        self.fuzzy = self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.actOnFuzzy)

    def actOnFuzzy(self, selected, client):
        if self!=client: return
        self.fuzzy.deactivate(self)
        self.display.open(selected)

    def setFuzzyData(self):

        notes=self.window.plugin.tables.getAll('notes')
        if len(notes)==0: return
        names=[n['title'] for n in notes]
        nids=[n['id'] for n in notes]

        self.fuzzy.setData(self, nids, names)

    def toggle(self):
        self.setFuzzyData()
        self.fuzzy.toggle(self)
