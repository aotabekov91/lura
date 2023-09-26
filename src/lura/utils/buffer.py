import os
import hashlib
from plug.qt.utils import Buffer as Base

class Buffer(Base):

    def setID(self, path, model):

        if not model in self.buffers:
            uid=self.getID(path)
            if uid:
                model.setId(uid)

    def getID(self, path):

        if os.path.isfile(path):
            path=os.path.expanduser(path)
            file_hash = hashlib.md5()
            with open(path, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(4096)
            return file_hash.hexdigest()
