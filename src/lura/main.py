from plug.qt import plugs, Plug
from plug.plugs.parser import Parser

class Lura(Plug):

    isMainApp=True

    def loadModer(self):

        self.moder.load(
                plugs=[
                    plugs.Exec,
                    plugs.Input,
                    plugs.Picky, 
                    plugs.Normal, 
                    plugs.Command, 
                    ]
                )

    def setup(self): 

        super().setup()
        self.setParser()
        self.loadModer()

    def setParser(self):

        self.parser=Parser(self)
        self.parser.addArgument(
                'source', nargs='?', default=None)

    def activate(self):

        self.moder.load()
        a, u = self.parser.parse()
        self.open(source=a.source)
        super().activate()

def run():

    app=Lura()
    app.activate()
