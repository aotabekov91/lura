from plug.qt import AppPlug

class Lura(AppPlug):

    def setParser(self):

        super().setParser()
        self.parser.addArgument(
                'source', 
                nargs='?', 
                default=None
                )

    def activate(self):

        super().activate()
        a, u = self.parser.parse()
        self.ui.handler.open(source=a.source)

def run():

    app=Lura()
    app.activate()
    app.run()
