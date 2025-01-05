from plug import Plug, tag

class WordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        if self.app.running:
            self.addSubmode()
        else:
            self.app.appIsLaunched.connect(
                    self.addSubmode)

    def addSubmode(self):
        visual=self.app.plugman.getPlug('Visual')
        if visual:
            visual.addAgent('word', self)

    def addAgent(self, action, obj, agent):
        if not obj in self.m_agents:
            self.m_agents[obj]={}
        self.m_agents[obj][action]=agent

    def getAgent(self, action=None, view=None, only_obj=False):
        if view:
            for klass in view.__class__.__mro__:
                name=klass.__name__
                obj=self.m_agents.get(name, {})
                if obj and only_obj:
                    return obj
                elif obj:
                    actioner=obj.get(action, None)
                    if actioner:
                        return actioner

    def delegate(self, action=None, view=None, **kwargs):
        if view is None:
            view=self.app.stateman.view()
        agent=self.getAgent(action=action, view=view)
        if agent:
            agent.delegate(action=action, view=view, **kwargs)

    @tag("<c-w>(visual)")
    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view, only_obj=True)
        if agent:
            self.app.stateman.setSubmode(
                    submode="word", submoder=self)
            self.delegate(action='start', view=view, **kwargs)

    @tag("<c-w>/<c-[>/<escape>(visual[word])")
    def octivate(self, **kwargs):
        self.app.stateman.setSubmode()
        self.delegate(action='finish', **kwargs)

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
