import os
import hashlib
from plug.qt.plugs.render import Render

from .view import View
from .model import Model

class PdfRender(Render):

    def setId(self, path, model):

        if os.path.isfile(path):
            path=os.path.expanduser(path)
            file_hash = hashlib.md5()
            with open(path, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(4096)
            dhash=file_hash.hexdigest()
            model.setId(dhash)

    def isCompatible(self, path):
        
        if path:
            path=path.lower()
            return path.endswith('pdf')

    def readFile(self, path):

        if self.isCompatible(path):
            return Model(path)

    def readModel(self, model):

        if model:
            path=model.filePath()
            if self.isCompatible(path):
                view=View(self.app)
                view.setModel(model)
                return view
