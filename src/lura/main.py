import plugs_qt
import plugs_fitz

from lura import core
from plug_qt import App

class Lura(App):

    def activate(self):
        plugs = [
            core.pdf_fitz.PdfFitz,
            plugs_fitz.FitzRotate,
            plugs_fitz.FitzGrayScale,
            plugs_fitz.FitzTrim,
            plugs_fitz.FitzLinks,
            plugs_fitz.FitzHints,
            plugs_fitz.FitzWords,
            plugs_fitz.FitzOutline,
            plugs_fitz.FitzSearch,
            plugs_fitz.FitzAnnotate,
            plugs_fitz.FitzBlocks,
            plugs_qt.Outline,
        ]
        self.plugman.load(plugs)
        super().activate()


def run():
    app = Lura()
    app.activate()
    app.run()
