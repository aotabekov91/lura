from plug import Plug

class ViewCopy(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, obj=None):
        if name is None and obj:
            name=obj.__class__.__name__
        return self.m_agents.get(name, None)

    def copy(self, obj):
        copier=self.getAgent(obj=obj)
        if copier:
            return copier.copy(obj)
