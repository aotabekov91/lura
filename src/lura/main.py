from plug.qt import Plug
from plug.plugs.parser import Parser
from plug.qt.plugs.moder import Moder
from plug.qt.plugs.picky import Picky
from plug.qt.plugs.normal import Normal

# from ohu.djvu import Djvu
from ohu.image_qt import ImageQt
from ohu.media_qt import MediaQt
from ohu.pdf_fitz import PdfFitz

class Lura(Plug):

    def loadModer(self):

        self.moder.load(
                plugs=set([
                    Picky, 
                    Normal, 
                    # Djvu,
                    ImageQt,
                    MediaQt,
                    PdfFitz,
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
                '-p', '--page', default=None)
        self.parser.addArgument(
                '-x', '--x-axis', default=0)
        self.parser.addArgument(
                '-y', '--y-axis', default=0)
        self.parser.addArgument(
                '-n', '--naked', default=False)
        self.parser.addArgument(
                'source', nargs='?', default=None)

    def parse(self):

        a, u = self.parser.parse()
        if not a.naked:
            self.moder.load()
        self.open(source=a.source)

            # a, **u)
        # view=self.display.currentView()
        # if view and a.page:
        #     view.goto(
        #             a.page, 
        #             a.xaxis, 
        #             a.yaxis)

def run():

    app=Lura()
    app.run()
