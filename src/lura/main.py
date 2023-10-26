from plug.qt import Plug
from ohu.pdf import PdfRender
from plug.plugs.parser import Parser
from lura.utils.normal import Normal
from plug.qt.plugs.moder import Moder
from plug.qt.plugs.picky import Picky

class Lura(Plug):

    def loadModer(self):

        self.moder.load(
                plugs=set([
                    Picky, 
                    Normal, 
                    PdfRender,
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
                'file', nargs='?')
        self.parser.addArgument(
                '-p', '--page', default=None)
        self.parser.addArgument(
                '-x', '--x-axis', default=0)
        self.parser.addArgument(
                '-y', '--y-axis', default=0)
        self.parser.addArgument(
                '-n', '--naked', default=False)

    def open(self, path, **kwargs):

        m=self.buffer.load(path)
        self.display.open(
                model=m, **kwargs)

    def parse(self):

        a, u = self.parser.parse()
        if not a.naked:
            self.moder.load()

    def launch(self):

        super().launch()
        a, u = self.parser.parse()
        if a.file:
            self.open(a.file)
            view=self.display.currentView()
            if view and a.page:
                view.goto(
                        a.page, 
                        a.xaxis, 
                        a.yaxis)

def run():

    app=Lura()
    app.run()
