import os

from qapp.app import Buffer
from ..render import PdfDocument

class LuraBuffer(Buffer):

    def getHash(self, path):

        if os.path.isfile(filePath):

            path=os.path.expanduser(path)
            file_hash = hashlib.md5()
            with open(filePath, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(4096)

            return file_hash.hexdigest()

    def load(self, path):

        path=os.path.abspath(path)

        if path in self.buffers:
            return self.buffers[path]

        buffer=PdfDocument(path)
        if buffer.readSuccess():
            self.buffers[path]=buffer
            dhash=self.getHash(path)
            if dhash:
                buffer.setParent(self.app)
                buffer.setHash(dhash)
                buffer.setId(dhash)
                self.bufferCreated.emit(buffer)
                return buffer