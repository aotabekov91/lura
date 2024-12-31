from PyQt6 import QtCore

from plug import Plug, tag

class Normal(Plug, QtCore.QObject):

    zoomChanged = QtCore.pyqtSignal(object, object)
    positionChanged = QtCore.pyqtSignal(object, object)

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, action, name, agent):
        if not action in self.m_agents:
            self.m_agents[action]={}
        self.m_agents[action][name]=agent

    def getAgent(self, action=None, view=None):
        if view:
            holder=self.m_agents.get(action, {})
            for klass in view.__class__.__mro__:
                name=klass.__name__
                agent=holder.get(name, None)
                if agent:
                    return agent

    def activate(
            self, 
            view=None, 
            action=None, 
            kind='goTo', 
            **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view:
            func=getattr(view, action, None)
            agent=self.getAgent(action=action, view=view)
            if agent:
                agent.activate(
                        action=action, view=view, kind=kind, **kwargs)
            elif func:
                func(action=action, kind=kind, **kwargs)

    def currentPosition(self, view):
        agent=self.getAgent(action='goTo', view=view)
        if agent:
            return agent.currentPosition(view=view)
        return {}

    def currentZoom(self, view):
        agent=self.getAgent(action='zoom', view=view)
        if agent:
            return agent.currentZoom(view=view)
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

    @tag('<c-[>/<escape>(normal)')
    def octivate(self):
        selection=self.app.plugman.getPlug('Selection')
        if selection:
            selection.cleanUpSelection()

    @tag('ts(normal)')
    def toggleStatusbar(self):
        self.app.view.bar.toggle()

    @tag('@(normal)')
    def activateSubview(self):
        subview=self.app.stateman.subview()
        if subview:
            subview.activate()

    @tag("zi(normal)")
    def zoomIn(self, xrange=[1,], **kwargs):
        self.activate(action='zoom', kind="in", xrange=xrange, **kwargs)

    @tag("zo(normal)")
    def zoomOut(self, xrange=[1,], **kwargs):
        self.activate(action='zoom', kind="out", xrange=xrange, **kwargs)

    @tag("zw(normal)")
    def zoomToWidth(self, **kwargs):
        self.activate(action='zoom', kind="width", **kwargs)

    @tag("za(normal)")
    def zoomToAdjust(self, **kwargs):
        self.activate(action='zoom',kind="adjust", **kwargs)

    @tag("zh(normal)")
    def zoomToHeight(self, **kwargs):
        self.activate(action='zoom', kind="height", **kwargs)
