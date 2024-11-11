from PyQt6 import QtCore

from plug import Plug

class FitzSelection(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        selector=self.app.plugman.plugs.get('Selection')
        if selector:
            selector.addAgent('FitzView', self)

    def select(self, view, data):
        #todo
        print(data)
        return data
