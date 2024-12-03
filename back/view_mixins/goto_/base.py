from PyQt6 import QtCore

from plug import tag


class Go:

    canGo = True
    positionChanged = QtCore.pyqtSignal()

    def go(
        self,
        *args,
        kind=None,
        mode=None,
        xrange=None,
        **kwargs,
    ):
        n = "goTo"
        func = getattr(self, n, None)
        if mode:
            n = mode + n[0].title() + n[1:]
            func = getattr(self, n, None)
        if kind:
            n = n + kind[0].title() + kind[1:]
            func = getattr(self, n, func)
        if func:
            func(
                *args,
                kind=kind,
                xrange=xrange,
                **kwargs,
            )

    @tag("G(normal)[^]")
    def goto(self, xrange=None, **kwargs):
        if not xrange:
            func = getattr(self, "goToLast", None)
            if func:
                func(xrange=xrange, **kwargs)
        else:
            self.go(xrange=xrange, **kwargs)

    @tag("gg(normal)[^]")
    def goFirst(self):
        self.go(kind="first")

    @tag("k(normal)[^]")
    def goUp(self, xrange=[1], **kwargs):
        self.go(kind="up", xrange=xrange)

    @tag("j(normal)[^]")
    def goDown(self, xrange=[1], **kwargs):
        self.go(kind="down", xrange=xrange)

    @tag("h(normal)[^]")
    def goLeft(self, xrange=[1], **kwargs):
        self.go(kind="left", xrange=xrange)

    @tag("l(normal)[^]")
    def goRight(self, xrange=[1], **kwargs):
        self.go(kind="right", xrange=xrange)

    @tag("n(normal)[^]")
    def goNext(self, xrange=[1], **kwargs):
        self.go(kind="next", xrange=xrange)

    @tag("p(normal)[^]")
    def goPrev(self, xrange=[1], **kwargs):
        self.go(kind="prev", xrange=xrange)

    @tag("[(normal)[^]")
    def goPrevLeap(self, xrange=[1], **kwargs):
        self.go(
            kind="prev",
            xrange=xrange,
            mode="leaper",
        )

    @tag("](normal)[^]")
    def goNextLeap(self, xrange=[1], **kwargs):
        self.go(
            kind="next",
            xrange=xrange,
            mode="leaper",
        )
