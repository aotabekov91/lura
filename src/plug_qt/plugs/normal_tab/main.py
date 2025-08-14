from plug import Plug, tag

class TabNormal(Plug):

    prefix_keys=["<c-t>(normal)"]

    def delegate(self, view=None, action=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        manager=None
        while view is not None:
            name=view.__class__.__name__
            if name=='TabView':
                manager=view
                break
            elif view is None:
                break
            else:
                view=view.manager()
        if manager:
            functor=getattr(manager, action, None)
            if functor:
                functor(**kwargs)

    @tag("gg(normal)")
    def goFirst(self, **kwargs):
        self.delegate(action='goTo', kind="first", **kwargs)

    @tag("G(normal)") # todo: go to last does not work; but go to number works
    def goToLast(self, xrange=None, **kwargs):
        kind=None
        if not xrange:
            kind='last'
        self.delegate(action='goTo', kind=kind, xrange=xrange, **kwargs)

    @tag("h/p(normal)")
    def goLeft(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="left", xrange=xrange, **kwargs)

    @tag("l/n(normal)")
    def goRight(self, xrange=[1], **kwargs):
        self.delegate(action='goTo', kind="right", xrange=xrange, **kwargs)

    @tag("J/K(normal)")
    def moveTo(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', xrange=xrange, **kwargs)

    @tag("H(normal)")
    def moveToLeft(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', kind="left", xrange=xrange, **kwargs)

    @tag("L(normal)")
    def moveToRight(self, xrange=[1], **kwargs):
        self.delegate(action='moveTo', kind="right", xrange=xrange, **kwargs)

    @tag("t(normal)")
    def create(self, focus=True, **kwargs):
        return self.delegate(action='create', focus=focus, **kwargs)

    @tag("c(normal)")
    def close(self, **kwargs):
        self.delegate(action='close', **kwargs)

    @tag("x/X(normal)")
    def flipTo(self, **kwargs):
        self.delegate(action='flipTo', **kwargs)
