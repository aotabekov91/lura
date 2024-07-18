import plugs_qt
import plugs_fitz

from plug_qt import App
from lura import pdf_fitz

class Lura(App):

    def activate(self):
        plugs = [
            # pdf_fitz.PdfFitz,

            plugs_fitz.FitzRotate,
            plugs_fitz.FitzGrayScale,
            plugs_fitz.FitzCopy,
            plugs_fitz.FitzTrim,
            plugs_fitz.FitzLinks,
            plugs_fitz.FitzHints,
            plugs_fitz.FitzWords,
            # plugs_fitz.FitzOutline,
            # plugs_fitz.FitzSearch,
            plugs_fitz.FitzAnnotate,
            plugs_fitz.FitzBlocks,
            plugs_fitz.FitzYankWord,

            plugs_qt.Outline,
        ]

        self.plugman.addPlugs(plugs)
        super().activate()


def run():
    app = Lura()
    app.activate()
    app.run()
