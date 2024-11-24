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

    @tag("k(normal)")
    def goUp(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="up", xrange=xrange, **kwargs)

    @tag("j(normal)")
    def goDown(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="down", xrange=xrange, **kwargs)

    @tag("h(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="left", xrange=xrange, **kwargs)

    @tag("l(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="right", xrange=xrange, **kwargs)

    @tag("s(normal)")
    def splitHorizontally(self, **kwargs):
        self.activate(action='splitTo', kind="horizontal", **kwargs)

    @tag("v(normal)")
    def splitVertically(self, **kwargs):
        self.activate(action='splitTo', kind="vertical", **kwargs)

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="next", xrange=xrange, **kwargs)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="prev", xrange=xrange, **kwargs)
        
    @tag("zk(normal)")
    def zoomTopUp(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="up", xrange=xrange, **kwargs)

    @tag("zK(normal)")
    def zoomTopDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="down", inc=False, xrange=xrange, **kwargs)

    @tag("zj(normal)")
    def zoomDown(self, xrange=[1], **kwargs):
        self.activate(action='zoomTo', kind="down", xrange=xrange, **kwargs)

    @tag("zj(normal)")
    def viewZoomInDown(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="down", xrange=xrange)

    @tag("zJ(normal)")
    def viewZoomOutDown(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="down", inc=False, xrange=xrange)

    @tag("zl(normal)")
    def viewZoomInRight(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="right", xrange=xrange)

    @tag("zL(normal)")
    def viewZoomOutRight(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="right", inc=False, xrange=xrange)

    @tag("zh(normal)")
    def viewZoomInLeft(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="left", xrange=xrange)

    @tag("zH(normal)")
    def viewZoomOutLeft(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="left", inc=False, xrange=xrange)



    @tag("<c-k>(normal)")
    def goBlockup(self, xrange=[1], **kwargs):
        self.activate(kind="goToBlockup", xrange=xrange)

    @tag("<c-j>(normal)")
    def goBlockdown(self, xrange=[1], **kwargs):
        self.activate(kind="goToBlockdown", xrange=xrange)

    @tag("<c-h>(normal)")
    def goBlockleft(self, xrange=[1], **kwargs):
        self.activate(kind="goToBlockleft", xrange=xrange)

    @tag("<c-l>(normal)")
    def goBlockRight(self, xrange=[1], **kwargs):
        self.activate(kind="goToBlockright", xrange=xrange)

    # @tag("gg(normal)")
    # def viewGoToFirst(self, **kwargs):
    #     self.viewGoTo(kind="first")

    @tag("x(normal)")
    def viewFlip(self):
        new, current = self.m_layout.swap()
        if new and new.view:
            new.view.activate()

    @tag("e(normal)")
    def equalizeRatio(self):
        self.m_layout.equalize()


    @tag("~gW(normal)")
    def viewMoveTo(self, xrange=None, **kwargs):
        return self.m_layout.move(xrange=xrange, **kwargs)

    @tag("K(normal)")
    def viewMoveToUp(self, xrange=[1]):
        self.viewMoveTo(kind="up", xrange=xrange)

    @tag("J(normal)")
    def viewMoveToDown(self, xrange=[1]):
        self.viewMoveTo(kind="down", xrange=xrange)

    @tag("H(normal)")
    def viewMoveToLeft(self, xrange=[1]):
        self.viewMoveTo(kind="left", xrange=xrange)

    @tag("L(normal)")
    def viewMoveToRight(self, xrange=[1]):
        self.viewMoveTo(kind="right", xrange=xrange)

    @tag("c(normal)")
    def closeView(self, v=None, **kwargs):
        l = self.m_layout
        p = l.findSibling(kind="prev")
        n = l.findSibling(kind="next")
        v = v or self.current
        l.removeView(v)
        if p and v != p:
            p.activate()
        elif n:
            n.activate()
