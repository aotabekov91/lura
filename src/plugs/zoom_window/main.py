from plug import Plug, tag

class WindowNormal(Plug):

    prefix_keys=["<c-w>(normal)"]

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def findAgent(self, view):
        while view:
            manager=view.manager()
            agent=self.getAgent(view=view)
            if agent:
                return agent, view
            view=manager
        return None, None 

    def goTo(self, view=None, kind='goTo', **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent, window=self.findAgent(view)
        if agent:
            agent.activate(window=window, kind=kind, **kwargs)

    @tag("G(normal)")
    def goToLast(self, xrange=None, **kwargs):
        kind='goTo'
        if not xrange:
            kind='goToLast'
        self.goTo(xrange=xrange, kind=kind, **kwargs)

    @tag("gg(normal)")
    def goFirst(self):
        self.goTo(kind="goToFirst")

    @tag("k/<c-<space>>(normal)")
    def goUp(self, xrange=[1], **kwargs):
        self.goTo(kind="goToUp", xrange=xrange)

    @tag("j/<space>(normal)")
    def goDown(self, xrange=[1], **kwargs):
        self.goTo(kind="goToDown", xrange=xrange)

    @tag("h(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.goTo(kind="goToLeft", xrange=xrange)

    @tag("l(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.goTo(kind="goToRight", xrange=xrange)

    @tag("<c-k>(normal)")
    def goBlockup(self, xrange=[1], **kwargs):
        self.goTo(kind="goToBlockup", xrange=xrange)

    @tag("<c-j>(normal)")
    def goBlockdown(self, xrange=[1], **kwargs):
        self.goTo(kind="goToBlockdown", xrange=xrange)

    @tag("<c-h>(normal)")
    def goBlockleft(self, xrange=[1], **kwargs):
        self.goTo(kind="goToBlockleft", xrange=xrange)

    @tag("<c-l>(normal)")
    def goBlockRight(self, xrange=[1], **kwargs):
        self.goTo(kind="goToBlockright", xrange=xrange)

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        self.goTo(kind="goToNext", xrange=xrange)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        self.goTo(kind="goToPrev", xrange=xrange)

    @tag("zk(normal)")
    def viewZoomInUp(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="up", xrange=xrange)

    @tag("zK(normal)")
    def viewZoomOutUp(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="up", inc=False, xrange=xrange)

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

    # @tag("gg(normal)")
    # def viewGoToFirst(self, **kwargs):
    #     self.viewGoTo(kind="first")

    @tag("G(normal)")
    def viewGoToLast(self, xrange=None, **kwargs):
        self.goTo(xrange=xrange, kind="last")

    @tag("v(normal)")
    def splitVertically(self):
        self.split(kind="vertical")

    @tag("s(normal)")
    def splitHorizontally(self):
        self.split(kind="horizontal")

    @tag("k(normal)")
    def viewGoToUp(self):
        self.goTo(kind="up")

    @tag("j(normal)")
    def viewGoToDown(self):
        self.goTo(kind="down")

    @tag("l(normal)")
    def viewGoToRight(self):
        self.goTo(kind="right")

    @tag("h(normal)")
    def viewGoToLeft(self):
        self.goTo(kind="left")

    @tag("n(normal)")
    def viewGoToNext(self):
        self.goTo(kind="next")

    @tag("p(normal)")
    def goToPrevView(self):
        self.goTo(kind="prev")

    @tag("x(normal)")
    def viewFlip(self):
        new, current = self.m_layout.swap()
        if new and new.view:
            new.view.activate()

    @tag("e(normal)")
    def equalizeRatio(self):
        self.m_layout.equalize()

    @tag("f(normal)")
    def toggleSplit(self):
        self.m_layout.toggleSplit()


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
