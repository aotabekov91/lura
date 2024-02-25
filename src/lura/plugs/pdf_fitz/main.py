from gizmo import plug

from .view import FitzView
from .model import FitzModel

class PdfFitz(plug.Plug):

    def setup(self):

        super().setup()
        self.app.handler.addViewer(
                FitzView)
        self.app.handler.addModeller(
                FitzModel)
