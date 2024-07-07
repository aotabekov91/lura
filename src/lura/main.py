import faulthandler
from lura import core
from plug_qt import App

from fitz_plugs import Rotate

class Lura(App):

    def activate(self):
        p = [
            core.pdf_fitz.PdfFitz,
            Rotate,
        ]
        self.plugman.load(p)
        super().activate()


def run():
    faulthandler.enable(all_threads=True)
    app = Lura()
    app.activate()
    app.run()
