from plug.qt import AppPlug

from .plugs.image_qt import ImageQt
from .plugs.pdf_fitz import PdfFitz
from .plugs.files import FileBrowser

class Lura(AppPlug):

    def activate(self):

        p=[
           ImageQt,
           PdfFitz,
           FileBrowser,
          ]
        self.ui.moder.load(p)
        self.ui.show()

def run():

    app=Lura()
    app.activate()
    app.run()
