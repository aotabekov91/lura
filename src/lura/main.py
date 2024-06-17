import faulthandler
from lura import core
from lura.qt import plug

class Lura(plug.app.AppPlug):
    pass

    # def activate(self):
    #     p = [
    #         core.pdf_fitz.PdfFitz,
    #     ]
    #     self.plugman.load(p)
    #     super().activate()


def run():
    faulthandler.enable(all_threads=True)
    app = Lura()
    app.activate()
    app.run()
