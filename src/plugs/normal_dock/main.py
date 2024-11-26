from plug import Plug, tag

class DockNormal(Plug):

    prefix_keys=["<c-d>(normal)"]

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

    @tag("k(normal)")
    def goUp(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="U", xrange=xrange, **kwargs)

    @tag("j(normal)")
    def goDown(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="D", xrange=xrange, **kwargs)

    @tag("h(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="L", xrange=xrange, **kwargs)

    @tag("l(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="R", xrange=xrange, **kwargs)

    @tag("<c-h>(normal)")
    def hide(self, xrange=None, **kwargs):
        self.activate(action='hide', xrange=xrange, **kwargs)

    @tag("<c-H>(normal)")
    def hideAll(self, **kwargs):
        self.activate(action='hide', kind='all', **kwargs)

    ###
    
    #todo :current:
    
    @tag("K(normal)")
    def moveToUp(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='U', xrange=xrange, **kwargs)

    @tag("J(normal)")
    def moveToDown(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='D', xrange=xrange, **kwargs)

    @tag("H(normal)")
    def moveToLeft(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='L', xrange=xrange, **kwargs)

    @tag("L(normal)")
    def moveToRight(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='R', xrange=xrange, **kwargs)

    @tag("x(normal)")
    def flipTo(self, **kwargs):
        self.activate(action='flipTo', **kwargs)

    @tag("X(normal)")
    def flipToWithNoFocus(self, **kwargs):
        self.activate(action='flipTo', focus=False, **kwargs)




    @tag("zk(normal)")
    def zoomTopUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='U', xrange=xrange, **kwargs)

    @tag("zK(normal)")
    def zoomTopDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='U', inc=False, xrange=xrange, **kwargs)

    @tag("zj(normal)")
    def zoomBottomUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='D', xrange=xrange, **kwargs)

    @tag("zJ(normal)")
    def zoomBottomDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='D', inc=False, xrange=xrange, **kwargs)

    @tag("zl(normal)")
    def zoomRightUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='R', xrange=xrange, **kwargs)

    @tag("zL(normal)")
    def zoomRightDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='R', inc=False, xrange=xrange, **kwargs)

    @tag("zh(normal)")
    def zoomLeftUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='L', xrange=xrange, **kwargs)

    @tag("zH(normal)")
    def zoomLeftDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind='L', inc=False, xrange=xrange, **kwargs)

    @tag("ze(normal)")
    def zoomToEqual(self, **kwargs):
        self.activate(action='zoomTo', kind="equal", **kwargs)

