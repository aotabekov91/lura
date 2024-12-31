from plug import Plug, tag

class WindowNormal(Plug):

    prefix_keys=["<c-w>(normal)"]

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

    def activate(
            self, 
            view=None, 
            action=None, 
            kind='goTo', 
            **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view:
            manager=view.manager()
            agent, window=self.findAgent(action, manager)
            if agent:
                return agent.activate(
                        window=window, 
                        kind=kind, 
                        action=action, 
                        **kwargs)

    @tag("gg(normal)")
    def goFirst(self, **kwargs):
        self.activate(action='goTo', kind="first", **kwargs)

    @tag("G(normal)")
    def goToLast(self, xrange=None, **kwargs):
        kind=None
        if not xrange:
            kind='last'
        return self.activate(action='goTo', kind=kind, xrange=xrange, **kwargs)

    @tag("k(normal)")
    def goUp(self, xrange=[1], **kwargs):
        return self.activate(action='goTo', kind="up", xrange=xrange, **kwargs)

    @tag("j(normal)")
    def goDown(self, xrange=[1], **kwargs):
        return self.activate(action='goTo', kind="down", xrange=xrange, **kwargs)

    @tag("h(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        return self.activate(action='goTo', kind="left", xrange=xrange, **kwargs)

    @tag("l(normal)")
    def goRight(self, xrange=[1], **kwargs):
        return self.activate(action='goTo', kind="right", xrange=xrange, **kwargs)

    @tag("s(normal)")
    def splitHorizontally(self, **kwargs):
        return self.activate(action='splitTo', kind="horizontal", **kwargs)

    @tag("v(normal)")
    def splitVertically(self, **kwargs):
        return self.activate(action='splitTo', kind="vertical", **kwargs)

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        return self.activate(action='goTo', kind="next", xrange=xrange, **kwargs)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        return self.activate(action='goTo', kind="prev", xrange=xrange, **kwargs)
        
    @tag("zk(normal)")
    def zoomTopUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="up", xrange=xrange, **kwargs)

    @tag("zK(normal)")
    def zoomTopDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="up", inc=False, xrange=xrange, **kwargs)

    @tag("zj(normal)")
    def zoomBottomUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="down", xrange=xrange, **kwargs)

    @tag("zJ(normal)")
    def zoomBottomDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="down", inc=False, xrange=xrange, **kwargs)

    @tag("zl(normal)")
    def zoomRightUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="right", xrange=xrange, **kwargs)

    @tag("zL(normal)")
    def zoomRightDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="right", inc=False, xrange=xrange, **kwargs)

    @tag("zh(normal)")
    def zoomLeftUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="left", xrange=xrange, **kwargs)

    @tag("zH(normal)")
    def zoomLeftDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="left", inc=False, xrange=xrange, **kwargs)

    @tag("ze(normal)")
    def zoomToEqual(self, **kwargs):
        self.activate(action='zoomTo', kind="equal", **kwargs)

    @tag("K(normal)")
    def moveToUp(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind="up", xrange=xrange, **kwargs)

    @tag("J(normal)")
    def moveToDown(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind="down", xrange=xrange, **kwargs)

    @tag("H(normal)")
    def moveToLeft(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind="left", xrange=xrange, **kwargs)

    @tag("L(normal)")
    def moveToRight(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind="right", xrange=xrange, **kwargs)

    @tag("x(normal)")
    def flipTo(self, **kwargs):
        self.activate(action='flipTo', **kwargs)

    @tag("X(normal)")
    def flipToWithNoFocus(self, **kwargs):
        self.activate(action='flipTo', focus=False, **kwargs)

    @tag("c(normal)")
    def closeView(self, **kwargs):
        self.activate(action='close', **kwargs)
