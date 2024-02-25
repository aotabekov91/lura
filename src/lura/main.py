from lura import plugs
from gizmo.qt import plug


class Lura(plug.app.AppPlug):
    def activate(self):
        p = [
            plugs.pdf_fitz.PdfFitz,
        ]
        self.moder.load(p)
        super().activate()


def run():
    app = Lura()
    app.activate()
    app.run()
