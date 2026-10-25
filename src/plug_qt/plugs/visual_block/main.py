from plug import Plug, tag, deleg

class BlockVisual(Plug):

    def delegate(self, action=None, view=None, **kwargs):
        if view is None:
            view=self.app.stateman.view()
        self.app.delegman.delegate(
                mode='visual', 
                submode='block', 
                view=view, 
                action=action, 
                data=kwargs)

    @deleg('activate@(visual[block])')
    @tag("<c-b>(visual)")
    def activate(self, view=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'visual', 'block', view, delegate='view')
        if agent:
            super().activate()
            self.app.stateman.setSubmode(
                    submode="block", submoder=self)
            self.app.delegman.delegate(
                    mode='visual', 
                    submode='block', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(visual[block])')
    @tag("<c-w>/<c-[>(visual[block])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='visual', 
                submode='block', 
                view=view, 
                action='octivate', 
                data=kwargs) 

    @tag("<c-j>(visual[block])")
    def jump(self):
        self.delegate(action='goTo', kind='jump')

    @tag("o(visual[block])")
    def goFirst(self, xrange=[1]):
        self.delegate(action='goTo', kind='first', xrange=xrange)

    @tag("$(visual[block])")
    def goLast(self, xrange=[1]):
        self.delegate(action='goTo', kind='last', xrange=xrange)

    @tag("k(visual[block])")
    def goUp(self, xrange=[1]):
        self.delegate(action='goTo', kind='up', xrange=xrange)

    @tag("j(visual[block])")
    def goDown(self, xrange=[1]):
        self.delegate(action='goTo', kind='down', xrange=xrange)

    @tag("l(visual[block])")
    def goRight(self, xrange=[1]):
        self.delegate(action='goTo', kind='right', xrange=xrange)

    @tag("h(visual[block])")
    def goLeft(self, xrange=[1]):
        self.delegate(action='goTo', kind='left', xrange=xrange)

    @tag("t(visual[block])")
    def toggleDirection(self):
        self.delegate(action='goTo', kind='toggle')
