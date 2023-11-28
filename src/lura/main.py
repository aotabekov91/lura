from plug.qt import plugs, Plug
from plug.plugs.parser import Parser

class Lura(Plug):

    isMainApp=True

    def loadModer(self):

        self.moder.load(
                plugs=[
                    plugs.Run,
                    plugs.Picky, 
                    plugs.Input,
                    plugs.Normal, 
                    plugs.Styler,
                    plugs.Command, 
                    plugs.GreenElf,
                    plugs.Powerline,
                    ]
                )

    def setup(self): 

        super().setup()
        self.setParser()
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

    app=Lura()
    app.activate()
