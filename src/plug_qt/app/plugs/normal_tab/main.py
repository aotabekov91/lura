from plug import Plug, tag

class TabNormal(Plug):

    prefix_keys=["<c-t>(normal)"]

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, action, name, agent):
        if not action in self.m_agents:
            self.m_agents[action]={}
        self.m_agents[action][name]=agent

    def getAgent(self, action=None, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        holder=self.m_agents.get(action, {})
        return holder.get(name, None)

    def findAgent(self, action, view):
        while view:
            manager=view.manager()
            agent=self.getAgent(action=action, view=view)
            if agent:
                return agent, view
            view=manager
        return None, None 

    def activate(self, view=None, action=None, kind='goTo', **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent, window=self.findAgent(action, view)
        if agent:
            agent.activate(window=window, kind=kind, action=action, **kwargs)

    @tag("gg(normal)")
    def goFirst(self, **kwargs):
        self.activate(action='goTo', kind="first", **kwargs)

    @tag("G(normal)")
    def goToLast(self, xrange=None, **kwargs):
        kind=None
        if not xrange:
            kind='last'
        self.activate(action='goTo', kind=kind, xrange=xrange, **kwargs)

    @tag("h/p(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="left", xrange=xrange, **kwargs)

    @tag("l/n(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="right", xrange=xrange, **kwargs)

    @tag("J/K(normal)")
    def moveTo(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', xrange=xrange, **kwargs)

    @tag("H(normal)")
    def moveToLeft(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind="left", xrange=xrange, **kwargs)

    @tag("L(normal)")
    def moveToRight(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind="right", xrange=xrange, **kwargs)

    @tag("t(normal)")
    def create(self, focus=True, **kwargs):
        return self.activate(action='create', focus=focus, **kwargs)

    @tag("c(normal)")
    def close(self, **kwargs):
        self.activate(action='close', **kwargs)

    @tag("x/X(normal)")
    def flipTo(self, **kwargs):
        self.activate(action='flipTo', **kwargs)
