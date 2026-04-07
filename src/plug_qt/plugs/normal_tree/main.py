from plug import Plug, tag, deleg

class TreeGoToNormal(Plug):

    @deleg('goTo@(normal)[TreeView]')
    def goTo(self, view=None, action=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view and action:
            functor=getattr(view, action, None)
            if functor:
                functor(**kwargs)

    @tag('L(normal)[TreeView]')
    def expandAll(self, **kwargs):
        self.goTo(action='expandAll', **kwargs)
        
    @tag('H(normal)[TreeView]')
    def collapseAl(self, **kwargs):
        self.goTo(action='collapseAll', **kwargs)

    @tag('pj(normal)[TreeView]')
    def parentDown(self, xrange=[1], **kwargs):
        self.goTo(xrange=xrange, action='parentDown', **kwargs)

    @tag('pk(normal)[TreeView]')
    def parentUp(self, xrange=[1], **kwargs):
        self.goTo(xrange=xrange, action='parentUp', **kwargs)

    @tag('rj(normal)[TreeView]')
    def rootDown(self, xrange=[1], **kwargs):
        self.goTo(xrange=xrange, action='rootDown', **kwargs)
        
    @tag('rk(normal)[TreeView]')
    def rootUp(self, xrange=[1], **kwargs):
        self.goTo(xrange=xrange, action='rootUp', **kwargs)

    @tag('sk(normal)[TreeView]')
    def siblingUp(self, xrange=[1], **kwargs):
        self.goTo(
                kind='up',
                xrange=xrange, 
                action='siblingGoTo', 
                **kwargs)

    @tag('sj(normal)[TreeView]')
    def siblingDown(self, xrange=[1], **kwargs):
        self.goTo(
                kind='down',
                xrange=xrange, 
                action='siblingGoTo', 
                **kwargs)
