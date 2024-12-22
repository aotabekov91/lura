from plug import Plug, tag

from .view import HelpView
from .model import HelpModel

class Help(Plug):

    def setup(self):
        super().setup()
        self.m_data={}
        self.addAgents()
        if self.app.running:
            self.gatherHelpFiles()
        else:
            self.app.appSoonStarts.connect(
                    self.gatherHelpFiles)

    def addAgents(self):
        self.app.buffman.addViewer(
                'HelpView', HelpView)
        self.app.buffman.addModeller(
                'HelpModel', HelpModel)

    def gatherHelpFiles(self):
        plugs=self.app.plugman.plugs
        for name, plug in plugs.items(): 
            name=name.lower()
            file=plug.getFile('help.md')
            if file:
                self.m_data[name]=file

    @tag('(exec)')
    def help(self, command, **kwargs):
        path=self.m_data.get(command, None)
        if path:
            self.app.buffman.open(source=path)
