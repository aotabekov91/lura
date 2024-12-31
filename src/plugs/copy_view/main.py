from plug import Plug

class ViewCopy(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if name is None and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def copy(self, obj):
        copier=self.getAgent(view=obj)
        if copier:
            return copier.copy(obj)
