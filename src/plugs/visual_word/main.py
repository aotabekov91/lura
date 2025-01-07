from plug import Plug, tag, deleg

class WordVisual(Plug):

    def delegate(self, action=None, view=None, **kwargs):
        if view is None:
            view=self.app.stateman.view()
        self.app.delegman.delegate(
                mode='visual', 
                submode='word', 
                view=view, 
                action=action, 
                data=kwargs)

    @deleg('activate@(visual[word])')
    @tag("<c-w>(visual)")
    def activate(self, view=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'visual', 'word', view, delegate='view')
        if agent:
            super().activate()
            self.app.stateman.setSubmode(
                    submode="word", submoder=self)
            self.app.delegman.delegate(
                    mode='visual', 
                    submode='word', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(visual[word])')
    @tag("<c-w>/<c-[>(visual[word])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='visual', 
                submode='word', 
                view=view, 
                action='octivate', 
                data=kwargs) 

    @tag("<c-j>(visual[word])")
    def jump(self):
        self.delegate(action='goTo', kind='jump')

    @tag("o(visual[word])")
    def goFirst(self, xrange=[1]):
        self.delegate(action='goTo', kind='first', xrange=xrange)

    @tag("$(visual[word])")
    def goLast(self, xrange=[1]):
        self.delegate(action='goTo', kind='last', xrange=xrange)

    @tag("k(visual[word])")
    def goUp(self, xrange=[1]):
        self.delegate(action='goTo', kind='up', xrange=xrange)

    @tag("j(visual[word])")
    def goDown(self, xrange=[1]):
        self.delegate(action='goTo', kind='down', xrange=xrange)

    @tag("l(visual[word])")
    def goRight(self, xrange=[1]):
        self.delegate(action='goTo', kind='right', xrange=xrange)

    @tag("h(visual[word])")
    def goLeft(self, xrange=[1]):
        self.delegate(action='goTo', kind='left', xrange=xrange)

    @tag("t(visual[word])")
    def toggleDirection(self):
        self.delegate(action='goTo', kind='toggle')
