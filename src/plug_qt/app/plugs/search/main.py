from plug import Plug

# todo

class Search(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)
