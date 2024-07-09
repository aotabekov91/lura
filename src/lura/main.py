import plugs_fitz

from lura import core
from plug_qt import App

class Lura(App):

    def activate(self):
        plugs = [
            core.pdf_fitz.PdfFitz,
            plugs_fitz.Rotate,
            plugs_fitz.GrayScale,
            plugs_fitz.TrimFitzView,
            plugs_fitz.FitzLinks,
            plugs_fitz.FitzHints,
        ]
        self.plugman.load(plugs)
        super().activate()


def run():
    app = Lura()
    app.activate()
    app.run()
