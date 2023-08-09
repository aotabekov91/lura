import os
import time
import hashlib

from PyQt5 import QtCore

class Hashman(QtCore.QObject):

    hashed=QtCore.pyqtSignal(str, str)

    def __init__(self, parent):

        super().__init__()
        self.parent=parent
        self.path=None

    def getHash(self, path):

        if os.path.isfile(path):

            path=os.path.expanduser(path)
            file_hash = hashlib.md5()

            with open(path, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(4096)

            return file_hash.hexdigest()

    def loop(self):

        while True:
            if self.path:
                dhash=self.getHash(self.path)
                self.hashed.emit(self.path, dhash)
                self.path=None
            else:
                time.sleep(1)
