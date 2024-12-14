from plug import Plug, tag

class DockNormal(Plug):

    prefix_keys=["<c-d>(normal)"]

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, action, agent):
        self.m_agents[action]=agent

    def getAgent(self, action=None):
        return self.m_agents.get(action, {})

    def activate(self, action=None, kind='goTo', **kwargs):
        manager=self.app.view.docks
        if manager:
            agent=self.getAgent(action=action)
            func=getattr(manager, action, None)
            if agent:
                agent.activate(
                        kind=kind, 
                        action=action, 
                        window=manager, 
                        **kwargs)
            elif func:
                func(
                        window=manager, 
                        kind=kind, 
                        action=action, 
                        **kwargs
                        )

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

    @tag("L(normal)")
    def moveToRight(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='R', xrange=xrange, **kwargs)
    
    @tag("K(normal)")
    def moveToUp(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='U', xrange=xrange, **kwargs)

    @tag("J(normal)")
    def moveToDown(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='D', xrange=xrange, **kwargs)

    @tag("H(normal)")
    def moveToLeft(self, xrange=[1], **kwargs):
        self.activate(action='moveTo', kind='L', xrange=xrange, **kwargs)

    @tag("x(normal)")
    def flipTo(self, **kwargs):
        self.activate(action='flipTo', **kwargs)

    @tag("X(normal)")
    def flipToWithNoFocus(self, **kwargs):
        self.activate(action='flipTo', focus=False, **kwargs)

    @tag("<c-h>(normal)")
    def hide(self, xrange=None, **kwargs):
        self.activate(action='hide', xrange=xrange, **kwargs)

    @tag("<c-H>(normal)")
    def hideAll(self, **kwargs):
        self.activate(action='hide', kind='all', **kwargs)

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
