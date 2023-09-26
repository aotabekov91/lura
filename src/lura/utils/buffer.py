import os
import hashlib
from plug.qt.utils import Buffer as Base

class Buffer(Base):

    def setID(self, path, model):

        model=self.buffers.get(path, None)
        if not model:
            uid=self.getHash(path)
            if uid:
                model.setId(uid)
                model.setHash(uid)

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
