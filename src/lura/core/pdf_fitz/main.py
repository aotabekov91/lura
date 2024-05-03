from gizmo import plug

from .model import FitzModel
from .view import FitzView


class PdfFitz(plug.Plug):
    def setup(self):
        super().setup()
        self.app.buffman.addViewer(FitzView)
        self.app.buffman.addModeller(FitzModel)
