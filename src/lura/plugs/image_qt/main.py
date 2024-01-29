from plug import Plug

from .view import ImageQtView
from .model import ImageQtModel

class ImageQt(Plug):

    def setup(self):

        super().setup()
        self.app.ui.handler.addViewer(
                ImageQtView)
        self.app.ui.handler.addModeller(
                ImageQtModel)
