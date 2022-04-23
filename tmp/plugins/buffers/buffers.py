from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.plugins.fuzzy import Fuzzy

class Buffers(QObject):

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.window=parent
        self.name='buffers'
        self.globalKeys={
                'Ctrl+c': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.fuzzy=self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.act)

    def setData(self):
        documents=[v.document() for v in self.window.buffer.getAllViews()]
        names=[d.filePath() for d in documents]
        self.fuzzy.setData(self, documents, names)

    def toggle(self):
        self.setData()
        self.fuzzy.activate(self)

    def act(self, document, fuzzyClient):
        if self==fuzzyClient:
            self.fuzzy.deactivate(self)
            self.window.open(document.filePath())
