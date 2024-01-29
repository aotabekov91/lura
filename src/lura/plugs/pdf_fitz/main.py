from plug import Plug

from .view import FitzView
from .model import FitzModel

class PdfFitz(Plug):

    def setup(self):

        super().setup()
        self.app.ui.handler.addViewer(
                FitzView)
        self.app.ui.handler.addModeller(
                FitzModel)
