from gizmo.ui.qt import plug

from lura import plugs


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
