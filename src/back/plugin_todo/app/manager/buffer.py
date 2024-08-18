import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Buffer(QObject):

    bufferCreated=pyqtSignal(object)

    def __init__(self, app):

        super().__init__()
        self.app=app

        self.watch=QFileSystemWatcher()
        self.watch.fileChanged.connect(self.on_fileChanged)

    def load(self, filePath): pass 

    def on_fileChanged(self, filePath): pass

    def watchFile(self, filePath): 

        self.watch.addPath(os.path.realpath(filePath))
