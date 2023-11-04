from PyQt5 import QtCore

from plug.qt import Plug
from plug.plugs.parser import Parser
from plug.qt.plugs.moder import Moder
from plug.qt.plugs.picky import Picky
from plug.qt.plugs.normal import Normal

from ohu.epub import Epub
from ohu.djvu import DjvuLibre
from ohu.image_qt import ImageQt
from ohu.media_qt import MediaQt
from ohu.pdf_fitz import PdfFitz

class Lura(Plug):

    def loadModer(self):

        self.moder.load(
                plugs=set([
                    Picky, 
                    Normal, 
                    Epub,
                    ImageQt,
                    MediaQt,
                    PdfFitz,
                    DjvuLibre,
                    ])
                )

    def setUIMan(self):

        super().setUIMan()
        self.uiman.setApp()
        self.uiman.setAppUI()

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
        self.open(source=a.source)
        if not a.naked:
            self.moder.load()

def run():

    app=Lura()
    app.run()
