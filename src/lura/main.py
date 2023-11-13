from PyQt5 import QtCore

from plug.qt import Plug
from plug.plugs.parser import Parser
from plug.qt.plugs.moder import Moder
from plug.qt.plugs.picky import Picky
from plug.qt.plugs.normal import Normal

# from ohu.epub import Epub
# from ohu.djvu import DjvuLibre
# from ohu.image_qt import ImageQt
# from ohu.media_qt import MediaQt
from ohu.pdf_fitz import PdfFitz

class Lura(Plug):

    main_app=True

    def loadModer(self):

        self.moder.load(
                plugs=set([
                    Picky, 
                    Normal, 
                    # Epub,
                    # ImageQt,
                    # MediaQt,
                    PdfFitz,
                    # DjvuLibre,
                    ])
                )

    def setup(self): 

        super().setup()
        self.setParser()
        self.setModer(Moder)
        self.loadModer()
        self.parse()

    def setParser(self):

        self.parser=Parser(self)
        self.parser.addArgument(
                '-n', '--naked', default=False)
        self.parser.addArgument(
                'source', nargs='?', default=None)

    def parse(self):

        a, u = self.parser.parse()
        if not a.naked:
            self.moder.load()
        self.open(source=a.source)

def run():

    raise
    app=Lura()
    app.run()
