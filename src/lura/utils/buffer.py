import os
from PyQt5 import QtCore
from plug.qt.utils import Buffer as Base

from .hashman import Hashman
from ..render import PdfDocument

class Buffer(Base):

    hashChanged=QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.hashman=Hashman(self)

    def setHash(self, path, dhash=None):

        if not dhash: 
            dhash=self.hashman.getHash(path)
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
        buffer=PdfDocument(path)
        if buffer.readSuccess():
            buffer.setParent(self.app)
            self.buffers[path]=buffer
            self.setHash(path)
            self.bufferCreated.emit(buffer)
            return buffer
