import faulthandler
import fitz_plugs
from lura import core
from plug_qt import App

class Lura(App):

    def activate(self):
        p = [
            core.pdf_fitz.PdfFitz,
            fitz_plugs.Rotate,
            fitz_plugs.GrayScale,
            fitz_plugs.TrimFitzView,
            fitz_plugs.FitzLinks,
        ]
        self.plugman.load(p)
        super().activate()


def run():
    faulthandler.enable(all_threads=True)
    app = Lura()
    app.activate()
    app.run()
