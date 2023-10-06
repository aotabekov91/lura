from plug.qt import Plug
from plug.qt.utils import Plugman
from plug.plugs.parser import Parser

from lura.utils.normal import Normal
from lura.render.pdf import PdfRender

class Lura(Plug):

    def setup(self): 

        super().setup()
        self.setPlugman(Plugman)
        self.uiman.setApp()
        self.uiman.setAppUI()
        self.setParser()
        self.setDefaultPlugs()

    def setDefaultPlugs(self):

        defaults=[Normal, PdfRender]
        self.plugman.loadPlugs(defaults)

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

    def open(self, path, **kwargs):

        if path:
            model=self.buffer.load(path)
            self.display.open(
                    model=model, **kwargs)

    def parse(self):

        if self.parser:
            a, u = self.parser.parse()
            self.open(a.file)
            view=self.display.currentView()
            if view and a.page:
                view.goto(a.page, 
                          a.xaxis, 
                          a.yaxis)

    def run(self):

        self.parse()
        super().run()

def run():

    app=Lura()
    app.run()
