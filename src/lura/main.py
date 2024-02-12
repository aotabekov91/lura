from plug.qt import AppPlug

from . import plugs

class Lura(AppPlug):

    def activate(self):

        p=[
           plugs.image_qt.ImageQt,
           plugs.pdf_fitz.PdfFitz,
           plugs.files.FileBrowser,
          ]
        self.ui.moder.load(p)
        super().activate()

def run():

    app=Lura()
    app.activate()
    app.run()
