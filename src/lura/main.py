from plug.qt import AppPlug

from . import plugs

class Lura(AppPlug):

    def activate(self):

        p=[
           plugs.pdf_fitz.PdfFitz,
          ]
        self.ui.moder.load(p)
        super().activate()

def run():

    app=Lura()
    app.activate()
    app.run()
