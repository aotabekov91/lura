from plug.qt import Plug
from plug.qt.plugs.exec import Exec
from plug.plugs.parser import Parser
from plug.qt.plugs.moder import Moder
from plug.qt.plugs.picky import Picky
from plug.qt.plugs.command import Command

from lura.utils.normal import Normal
from lura.render.pdf import PdfRender

class Lura(Plug):

    def loadModer(self):

        plugs=set([
            Exec, 
            Picky,
            Normal, 
            Command, 
            PdfRender,
            ])
        self.moder.load(plugs=plugs)
        print(self.moder.plugs.exec.actions)

    def setup(self): 

        super().setup()
        self.setParser()
        self.setModer()
        self.uiman.setApp()
        self.uiman.setAppUI()
        self.loadModer()

    def setModer(self):

        config=self.config.get(
                'Moder', {})
        self.moder=Moder(
                app=self,
                config=config,
                )

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
                view.goto(
                        a.page, 
                        a.xaxis, 
                        a.yaxis)

    def run(self):

        self.parse()
        super().run()

def run():

    app=Lura()
    app.run()
