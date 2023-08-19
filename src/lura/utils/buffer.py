import os

from PyQt5 import QtCore

from plug.qt.utils import Buffer as Base

from .hashman import Hashman
from ..render import PdfDocument

class Buffer(Base):

    hashChanged=QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setHashman()

    def setHashman(self):

        self.hash_thread=QtCore.QThread()

        self.hashman=Hashman(self)
        self.hashman.moveToThread(self.hash_thread)

        self.hash_thread.started.connect(self.hashman.loop)
        self.hashman.hashed.connect(self.setHash)
        QtCore.QTimer.singleShot(0, self.hash_thread.start)

    def setHash(self, path, dhash):

        if dhash:
            buffer=self.buffers.get(path)
            if buffer:
                buffer.setHash(dhash)
                buffer.setId(dhash)
                self.hashChanged.emit(buffer)

    def load(self, path):

        path=os.path.abspath(path)

        if path in self.buffers:
            return self.buffers[path]

        self.hashman.path=path

        buffer=PdfDocument(path)
        if buffer.readSuccess():
            buffer.setParent(self.app)
            self.buffers[path]=buffer
            self.bufferCreated.emit(buffer)
            return buffer
