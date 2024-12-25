from plug import Plug, tag

class TreeNormal(Plug):

    @tag('L(normal)[TreeView]')
    def expandAll(self, *args, **kwargs):
        self.activate(*args, action='expandAll', **kwargs)
        
    @tag('H(normal)[TreeView]')
    def collapseAl(self, *args, **kwargs):
        self.activate(*args, action='collapseAll', **kwargs)

    @tag('pj(normal)[TreeView]')
    def parentDown(self, xrange=[1], **kwargs):
        self.activate(xrange=xrange, action='parentDown', **kwargs)

    @tag('pk(normal)[TreeView]')
    def parentUp(self, xrange=[1], **kwargs):
        self.activate(xrange=xrange, action='parentUp', **kwargs)

    @tag('rj(normal)[TreeView]')
    def rootDown(self, xrange=[1], **kwargs):
        self.activate(xrange=xrange, action='rootDown', **kwargs)
        
    @tag('rk(normal)[TreeView]')
    def rootUp(self, xrange=[1], **kwargs):
        self.activate(xrange=xrange, action='rootUp', **kwargs)

    @tag('sk(normal)[TreeView]')
    def siblingUp(self, xrange=[1], **kwargs):
        self.activate(
                kind='up',
                xrange=xrange, 
                action='siblingGoTo', 
                **kwargs)

    @tag('sj(normal)[TreeView]')
    def siblingDown(self, xrange=[1], **kwargs):
        self.activate(
                kind='down',
                xrange=xrange, 
                action='siblingGoTo', 
                **kwargs)

    def activate(self, view=None, action=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view and action:
            functor=getattr(view, action, None)
            if functor:
                functor(**kwargs)
