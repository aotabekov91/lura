from plug import Plug, tag

class TileNormal(Plug):

    prefix_keys=["<c-w>(normal)"]

    def delegate(self, view=None, action=None, **kwargs):
        view=view or self.app.stateman.view()
        if view:
            kwargs['view']=view
            self.app.delegman.delegate(
                    mode='normal',
                    view=view.manager(),
                    action=action,
                    data=kwargs,)

    @tag("gg(normal)")
    def goFirst(self, **kwargs):
        self.delegate(action='goTo', kind="first", **kwargs)

    @tag("G(normal)")
    def goTo(self, xrange=None, **kwargs):
        if xrange:
            return self.delegate(
                    action='goTo', kind='xrange', xrange=xrange, **kwargs)
        else:
            return self.delegate(action='goTo', kind='last', **kwargs)

    @tag("k(normal)")
    def goUp(self, xrange=[1], **kwargs):
        return self.delegate(action='goTo', kind="up", xrange=xrange, **kwargs)

    @tag("j(normal)")
    def goDown(self, xrange=[1], **kwargs):
        return self.delegate(action='goTo', kind="down", xrange=xrange, **kwargs)

    @tag("h(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        return self.delegate(action='goTo', kind="left", xrange=xrange, **kwargs)

    @tag("l(normal)")
    def goRight(self, xrange=[1], **kwargs):
        return self.delegate(action='goTo', kind="right", xrange=xrange, **kwargs)

    @tag("s(normal)")
    def splitHorizontally(self, **kwargs):
        return self.delegate(action='splitTo', kind="horizontal", **kwargs)

    @tag("v(normal)")
    def splitVertically(self, **kwargs):
        return self.delegate(action='splitTo', kind="vertical", **kwargs)

    @tag("n(normal)")
    def goNext(self, xrange=[1], **kwargs):
        return self.delegate(action='goTo', kind="next", xrange=xrange, **kwargs)

    @tag("p(normal)")
    def goPrev(self, xrange=[1], **kwargs):
        return self.delegate(action='goTo', kind="prev", xrange=xrange, **kwargs)
        
    @tag("zk(normal)")
    def zoomTopUp(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="up", xrange=xrange, **kwargs)

    @tag("zK(normal)")
    def zoomTopDown(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="up", inc=False, xrange=xrange, **kwargs)

    @tag("zj(normal)")
    def zoomBottomUp(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="down", xrange=xrange, **kwargs)

    @tag("zJ(normal)")
    def zoomBottomDown(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="down", inc=False, xrange=xrange, **kwargs)

    @tag("zl(normal)")
    def zoomRightUp(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="right", xrange=xrange, **kwargs)

    @tag("zL(normal)")
    def zoomRightDown(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="right", inc=False, xrange=xrange, **kwargs)

    @tag("zh(normal)")
    def zoomLeftUp(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="left", xrange=xrange, **kwargs)

    @tag("zH(normal)")
    def zoomLeftDown(self, xrange=[1], **kwargs):
        self.delegate(action='zoomTo', kind="left", inc=False, xrange=xrange, **kwargs)

    @tag("ze(normal)")
    def zoomToEqual(self, **kwargs):
        self.delegate(action='zoomTo', kind="equal", **kwargs)

    @tag("K(normal)")
    def moveToUp(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', kind="up", xrange=xrange, **kwargs)

    @tag("J(normal)")
    def moveToDown(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', kind="down", xrange=xrange, **kwargs)

    @tag("H(normal)")
    def moveToLeft(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', kind="left", xrange=xrange, **kwargs)

    @tag("L(normal)")
    def moveToRight(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', kind="right", xrange=xrange, **kwargs)

    @tag("x(normal)")
    def flipTo(self, **kwargs):
        self.delegate(action='flipTo', **kwargs)

    @tag("X(normal)")
    def flipToWithNoFocus(self, **kwargs):
        self.delegate(action='flipTo', focus=False, **kwargs)

    @tag("c(normal)")
    def closeView(self, **kwargs):
        self.delegate(action='close', **kwargs)
