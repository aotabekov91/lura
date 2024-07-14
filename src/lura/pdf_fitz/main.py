import plug

from .view import FitzView
from .model import FitzModel

class PdfFitz(plug.Plug):
    def setup(self):
        super().setup()
        self.app.buffman.addViewer(
                'FitzView', FitzView)
        self.app.buffman.addModeller(
                'FitzModel', FitzModel)
