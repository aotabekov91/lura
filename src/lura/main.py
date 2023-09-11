from plug.qt import PlugApp

from .view import View
from .utils import Display, Buffer

class Lura(PlugApp):

    def __init__(self, **kwargs): 

        super().__init__(
            respond_port=True,
            initiate_stack=True,
            **kwargs
            )

    def setup(self): 

        super().setup()
        self.buffer=Buffer(self)
        self.setGUI(
                display_class=Display, 
                view_class=View)

    def initialize(self):

        super().initialize()
        self.parser=self.plugman.plugs.get(
                'Parser', None)

    def parse(self):

        if self.parser:
            a, u = self.parser.parse()
            view=self.window.main.display.currentView()
            if a.file:
                self.window.main.open(filePath=a.file)
            if a.page and view:
                view.goto(a.page, a.xaxis, a.yaxis)

    def run(self):

        self.parse()
        super().run()

def run():

    app=Lura()
    app.run()
