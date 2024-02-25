from gizmo import plug

from .model import FitzModel
from .view import FitzView


class PdfFitz(plug.Plug):
    def setup(self):
        super().setup()
        self.app.handler.addViewer(FitzView)
        self.app.handler.addModeller(FitzModel)
