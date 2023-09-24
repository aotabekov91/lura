from plug.qt import Plug
from plug.qt.utils import Plugman
from plug.plugs.parser import Parser

from .view import View
from .utils import Display, Buffer

class Lura(Plug):

    def setup(self): 

        super().setup()
        self.setPlugman(Plugman)
        self.uiman.setApp()
        self.uiman.setAppUI(Display, View)
        self.display=self.uiman.window.main.display
        self.buffer=Buffer(self)
        self.setParser()

    def setParser(self):

        self.parser=Parser(self)
        self.parser.addArgument('file', nargs='?')
        self.parser.addArgument('-p', '--page', default=None)
        self.parser.addArgument('-x', '--x-axis', default=0)
        self.parser.addArgument('-y', '--y-axis', default=0)

    def parse(self):

        if self.parser:
            a, u = self.parser.parse()
            view=self.uiman.window.main.display.currentView()
            if a.file:
                self.uiman.window.main.open(filePath=a.file)
            if a.page and view:
                view.goto(a.page, a.xaxis, a.yaxis)

    def run(self):

        self.parse()
        super().run()

def run():

    app=Lura()
    app.run()
