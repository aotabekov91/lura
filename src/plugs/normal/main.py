from PyQt6 import QtCore

from plug import Plug, tag

class Normal(Plug, QtCore.QObject):

    positionChanged = QtCore.pyqtSignal(object, object)

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

    def activate(self, view=None, action=None, kind='goTo', **kwargs):
        if not view:
            view=self.app.stateman.view()
        print(view, action, kind)
        func=getattr(view, action, None)
        agent=self.getAgent(action=action, view=view)
        if agent:
            agent.activate(view=view, kind=kind, **kwargs)
            data=agent.currentPosition(view=view)
            self.positionChanged.emit(view, data)
        elif func:
            func(kind=kind, **kwargs)

    def currentPosition(self, view):
        agent=self.getAgent(action='goTo', view=view)
        if agent:
            return agent.currentPosition(view=view)
        return {}

    @tag("G(normal)")
    def go(self, xrange=None, **kwargs):
        kind='goTo'
        if not xrange:
            kind='last'
        self.activate(action='goTo', xrange=xrange, kind=kind, **kwargs)

    @tag("gg(normal)")
    def goFirst(self):
        self.activate(action='goTo', kind="first")

    @tag("k/<vwheel_up>(normal)")
    def goUp(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="up", xrange=xrange)

    @tag("j/<vwheel_down>(normal)")
    def goDown(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="down", xrange=xrange)

    @tag("h(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="left", xrange=xrange)

    @tag("l(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="right", xrange=xrange)

    @tag("K/<c-<space>>(normal)")
    def goBlockup(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="blockup", xrange=xrange)

    @tag("J/<space>(normal)")
    def goBlockdown(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="blockdown", xrange=xrange)

    @tag("H(normal)")
    def goBlockleft(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="blockleft", xrange=xrange)

    @tag("L(normal)")
    def goBlockRight(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="blockright", xrange=xrange)

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="next", xrange=xrange)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind="prev", xrange=xrange)
