from plug import Plug, tag

class TreeNormalGoTo(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                'normal', None, 'TreeView', 'goTo', self.delegate)

    def delegate(self, view=None, action=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        print(view, action)
        if view and action:
            functor=getattr(view, action, None)
            if functor:
                functor(**kwargs)

    @tag('L(normal)[TreeView]')
    def expandAll(self, **kwargs):
        self.delegate(action='expandAll', **kwargs)
        
    @tag('H(normal)[TreeView]')
    def collapseAl(self, **kwargs):
        self.delegate(action='collapseAll', **kwargs)

    @tag('pj(normal)[TreeView]')
    def parentDown(self, xrange=[1], **kwargs):
        self.delegate(xrange=xrange, action='parentDown', **kwargs)

    @tag('pk(normal)[TreeView]')
    def parentUp(self, xrange=[1], **kwargs):
        self.delegate(xrange=xrange, action='parentUp', **kwargs)

    @tag('rj(normal)[TreeView]')
    def rootDown(self, xrange=[1], **kwargs):
        self.delegate(xrange=xrange, action='rootDown', **kwargs)
        
    @tag('rk(normal)[TreeView]')
    def rootUp(self, xrange=[1], **kwargs):
        self.delegate(xrange=xrange, action='rootUp', **kwargs)

    @tag('sk(normal)[TreeView]')
    def siblingUp(self, xrange=[1], **kwargs):
        self.delegate(
                kind='up',
                xrange=xrange, 
                action='siblingGoTo', 
                **kwargs)

    @tag('sj(normal)[TreeView]')
    def siblingDown(self, xrange=[1], **kwargs):
        self.delegate(
                kind='down',
                xrange=xrange, 
                action='siblingGoTo', 
                **kwargs)
