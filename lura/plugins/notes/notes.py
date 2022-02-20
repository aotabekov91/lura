from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .note import Note
from .display import Display
from .connect import DatabaseConnector

class Notes(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.display=Display(self, settings)
        self.s_settings=settings
        self.location='left'
        self.name = 'notes'
        self.globalKeys={
                'Ctrl+n': (
                    self.display.toggle,
                    self.window,
                    Qt.WindowShortcut)}
        self.setup()

    def setup(self):
        self.db = DatabaseConnector(self, self.window)
        self.window.noteCreated.connect(self.on_noteCreated)

    def get(self, nid):
        return self.db.get(nid)

    def getByDid(self, did):
        return self.db.getByDid(did)

    def new(self):
        note=Note()
        self.db.register(note)
        return note

    def on_noteCreated(self, note):
        self.db.register(note)
