from PyQt5 import QtCore
from plug.qt.utils import Buffer as Base

from .hashman import Hashman

class Buffer(Base):

    hashChanged=QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.hashman=Hashman(self)

    def setHash(self, path, dhash=None):

        if not dhash: 
            dhash=self.hashman.getHash(path)
        if dhash:
            model=self.buffers.get(path)
            if model:
                model.setHash(dhash)
                model.setId(dhash)
                self.hashChanged.emit(model)
