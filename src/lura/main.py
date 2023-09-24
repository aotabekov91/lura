from plug.qt import Plug
from plug.qt.utils import Plugman
from plug.plugs.parser import Parser

from .utils import Display, Buffer

class Lura(Plug):

    def setup(self): 

        super().setup()
        self.setPlugman(Plugman)
        self.uiman.setApp()
        self.uiman.setAppUI(Display, Buffer)
        self.setParser()

    def setParser(self):

        self.parser=Parser(self)
        self.parser.addArgument('file', nargs='?')
        self.parser.addArgument('-p', '--page', default=None)
        self.parser.addArgument('-x', '--x-axis', default=0)
        self.parser.addArgument('-y', '--y-axis', default=0)

    def open(self, path, **kwargs):

        model=self.buffer.load(path)
        self.display.open(model=model, **kwargs)

    def parse(self):

        if self.parser:
            a, u = self.parser.parse()
            if a.file:
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
