from plug.qt.plugs.render import Render

from .view import View
from .model import Model

class PdfRender(Render):

    def isCompatible(self, path):
        
        if path:
            return path.lower().endswith('pdf')

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
