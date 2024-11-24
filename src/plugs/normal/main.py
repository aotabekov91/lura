from PyQt6 import QtCore

from plug import Plug, tag

class Normal(Plug, QtCore.QObject):

    positionChanged = QtCore.pyqtSignal(object, object)

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def goTo(self, view=None, kind='goTo', **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.activate(view=view, kind=kind, **kwargs)
            data=agent.currentPosition(view=view)
            self.positionChanged.emit(view, data)

    def currentPosition(self, view):
        agent=self.getAgent(view=view)
        if agent:
            return agent.currentPosition(view=view)
        return {}

    @tag("G(normal)")
    def go(self, xrange=None, **kwargs):
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
