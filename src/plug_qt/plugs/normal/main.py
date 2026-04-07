from PyQt6 import QtCore

from plug import Plug, tag

class Normal(Plug, QtCore.QObject):

    stateChanged=QtCore.pyqtSignal(str, object, object)

    def delegate(self, action=None, view=None, **kwargs):
        view=view or self.app.stateman.view()
        self.app.delegman.delegate(
                mode='normal', view=view, action=action, data=kwargs)

    @tag("G(normal)")
    def go(self, xrange=None, **kwargs):
        if xrange is None:
            self.delegate(action='goTo', kind='last', **kwargs)
        else:
            self.delegate(
                    action='goTo', kind='xrange', xrange=xrange, **kwargs)

    @tag("gg(normal)")
    def goFirst(self):
        self.delegate(action='goTo', kind="first")

    @tag("k/<up>/<vwheel_up>(normal)")
    def goUp(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="up", xrange=xrange)

    @tag("j/<down>/<vwheel_down>(normal)")
    def goDown(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="down", xrange=xrange)

    @tag("h/<left>(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="left", xrange=xrange)

    @tag("l/<right>(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="right", xrange=xrange)

    @tag("K/<c-<space>>(normal)")
    def goBlockup(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="blockup", xrange=xrange)

    @tag("J/<space>(normal)")
    def goBlockdown(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="blockdown", xrange=xrange)

    @tag("H(normal)")
    def goBlockleft(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="blockleft", xrange=xrange)

    @tag("L(normal)")
    def goBlockRight(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="blockright", xrange=xrange)

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="next", xrange=xrange)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="prev", xrange=xrange)

    @tag('<c-[>/<escape>(normal)')
    def octivate(self):
        selection=self.app.plugman.getPlug('Selection')
        if selection:
            selection.clear()

    @tag('ts(normal)')
    def toggleStatusbar(self):
        self.app.view.bar.toggle()

    @tag('@(normal)')
    def activateSubview(self):
        subview=self.app.stateman.subview()
        if subview:
            manager=subview.manager()
            manager.activate()
            subview.activate(recursive=True)
            print(manager.activated, 'here')

    @tag("zi(normal)")
    def zoomIn(self, xrange=[1], **kwargs):
        self.delegate(action='zoom', kind="in", xrange=xrange, **kwargs)

    @tag("zo(normal)")
    def zoomOut(self, xrange=[1], **kwargs):
        self.delegate(action='zoom', kind="out", xrange=xrange, **kwargs)

    @tag("zw(normal)")
    def zoomToWidth(self, **kwargs):
        self.delegate(action='zoom', kind="width", **kwargs)

    @tag("za(normal)")
    def zoomToAdjust(self, **kwargs):
        self.delegate(action='zoom',kind="adjust", **kwargs)

    @tag("zh(normal)")
    def zoomToHeight(self, **kwargs):
        self.delegate(action='zoom', kind="height", **kwargs)

    @tag("r(normal)")
    def rotateView(self, xrange=[1], **kwargs):
        self.delegate(
                action='rotate', kind='view', xrange=xrange, **kwargs)

    @tag("R(normal)")
    def rotateItem(self, xrange=[1], **kwargs):
        self.delegate(
                action='rotate', kind='item', xrange=xrange, **kwargs)

    @tag("yy(normal)")
    def yankSelection(self, **kwargs):
        self.delegate(action='yank', kind='selection', **kwargs)

    def getState(self, view=None, state=None, **kwargs):
        if view and state:
            action=f'{state}State'
            agent=self.getAgent(action=action, view=view)
            if agent:
                return agent.activate(
                        action=action, view=view, **kwargs)
