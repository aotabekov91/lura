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

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="next", xrange=xrange, **kwargs)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="prev", xrange=xrange, **kwargs)
        
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
    def closeTab(self, **kwargs):
        self.activate(action='close', **kwargs)

    ####

    @tag("n(normal)[^]")
    def addAndGoToNewTab(self, focus=False, **kwargs):
        return self.addNewTab(focus=True, **kwargs)

    @tag("N(normal)")
    def addNewTab(self, focus=False, **kwargs):
        t = self.getNewTab(**kwargs)
        if focus and t:
            self.setView(t)
            t.activate()
        return t



    @tag("T(normal)")
    def addCopyTab(self, tab=None, **kwargs):
        c = self.getCopyTab(tab, **kwargs)
        if c:
            self.addView(c)
        return c

    @tag("t(normal)")
    def addAndGoToCopyTab(self, tab=None, **kwargs):
        c = self.addCopyTab(tab, **kwargs)
        if c:
            c.activate()
        return c

    @tag("c(normal)[^]")
    def closeCurrentTab(self):
        return self.tabClose()

    @tag("x(normal)[^]")
    def swapCurrent(self, **kwargs):
        self.setView(self.previous)

    @tag("l(normal)[^]")
    def tabGoToNext(self):
        self.tabGoTo(kind="next")

    @tag("h(normal)[^]")
    def tabGoToPrev(self):
        self.tabGoTo(kind="prev")

    @tag("H(normal)[^]")
    def tabMoveToLeft(self):
        self.tabMoveTo(kind="prev")

    @tag("L(normal)[^]")
    def tabMoveToRight(self):
        self.tabMoveTo(kind="next")

    @tag("gt(normal)[^]")
    def tabGoTo(self, xrange=[], kind=None):
        idx = self.currentIndex()
        if kind == "prev":
            xrange[-1] = max(0, idx - 1)
        elif kind == "next":
            xrange[-1] = idx + 1
            if xrange[-1] >= self.count():
                xrange[-1] = 0
            # xrange=min(self.count()-1, idx+1)
        elif kind == "first":
            xrange[-1] = 0
        elif kind == "last":
            xrange[-1] = self.count() - 1
        elif xrange is None:
            xrange[-1] = self.count() - 1
        elif not xrange:
            return
        else:
            xrange[-1] -= 1
        ntab = self.widget(xrange[-1])
        if ntab:
            ntab.activate()

    @tag("~gT(normal)[^]")
    def tabMoveTo(self, kind=None, xrange=None):
        c = self.currentIndex()
        if kind == "prev":
            xrange = max(0, c - 1)
        elif kind == "next":
            xrange = min(self.count() - 1, c + 1)
        elif type(xrange) == int:
            xrange[-1] -= 1
        elif xrange is None:
            xrange = self.count() - 1
        else:
            return
        w = self.widget(c)
        self.removeView(w)
        self.insertView(xrange, w)
        self.setView(w)

