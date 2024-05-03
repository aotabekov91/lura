from lura import core
from gizmo.ui.qt import plug

class Lura(plug.app.AppPlug):
    def activate(self):
        p = [
            core.pdf_fitz.PdfFitz,
        ]
        self.plugman.load(p)
        super().activate()


def run():
    app = Lura()
    app.activate()
    app.run()
