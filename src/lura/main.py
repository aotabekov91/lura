from plug.qt import Plug
from ohu.pdf import PdfRender
from plug.qt.plugs.run import Run
from plug.plugs.parser import Parser
from lura.utils.normal import Normal
from plug.qt.plugs.moder import Moder
from plug.qt.plugs.picky import Picky
from plug.qt.plugs.command import Command

class Lura(Plug):

    def loadModer(self):

        self.moder.load(
                plugs=set([
                    Run, 
                    Picky, 
                    Normal, 
                    Command, 
                    PdfRender,
                    ])
                )

    def setup(self): 

        super().setup()
        self.setParser()
        self.setModer(Moder)
        self.uiman.setApp()
        self.uiman.setAppUI()
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

        if path:
            model=self.buffer.load(path)
            self.display.open(
                    model=model, 
                    **kwargs)

    def parse(self):

        a, u = self.parser.parse()
        self.open(a.file)
        view=self.display.currentView()
        if view and a.page:
            view.goto(
                    a.page, 
                    a.xaxis, 
                    a.yaxis)
        if not a.naked:
            self.moder.load()

def run():

    app=Lura()
    app.run()
