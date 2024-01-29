from plug.qt import AppPlug
from gizmo.vimo.view.app import AppView

from .plugs.image_qt import ImageQt
from .plugs.pdf_fitz import PdfFitz
from .plugs.files import FileBrowser

class Lura(AppPlug):

    def setView(self):
        super().setView(AppView)

    def setup(self):

        super().setup()
        p=[
           ImageQt,
           PdfFitz,
           FileBrowser,
          ]
        self.ui.moder.load(p)

def run():

    app=Lura()
    app.activate()
    app.run()
