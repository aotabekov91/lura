from plug import Plug, tag

class Rotate(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def addAgent(self, name, rotator):
        self.m_agents[name]=rotator

    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view:
            agent=self.getAgent(view=view)
            if agent:
                agent.activate(view=view, **kwargs)

    @tag("r(normal)")
    def rotateView(self, xrange=None, **kwargs):
        self.activate(xrange=xrange, **kwargs)

    @tag("R(normal)")
    def rotateItem(self, xrange=None, **kwargs):
        self.activate(xrange=xrange, only_item=True, **kwargs)
