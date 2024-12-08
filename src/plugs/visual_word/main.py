from plug import Plug, tag

class WordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, visualizer):
        self.m_agents[name]=visualizer

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag(["<c-w>(visual)", "<c-w>/<c-[>(visual[word])"])
    def toggle(self):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            submode=self.app.stateman.activate(
                    submode="word", toggle_submode=True)
            if submode=='word':
                if self.check('visualize', agent):
                    agent.visualize(view)
            else:
                if self.check('unvisualize', agent):
                    agent.unvisualize(view)
                self.app.stateman.activate()

    @tag("<c-j>(visual[word])")
    def jump(self):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(view, kind='jump')

    @tag("o(visual[word])")
    def goFirst(self, xrange=[1]):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='first')

    @tag("$(visual[word])")
    def goLast(self, xrange=[1]):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='last')

    @tag("k(visual[word])")
    def goUp(self, xrange=[1]):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='up')

    @tag("j(visual[word])")
    def goDown(self, xrange=[1]):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='down')

    @tag("l(visual[word])")
    def goRight(self, xrange=[1]):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='right')

    @tag("h(visual[word])")
    def goLeft(self, xrange=[1]):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='left')

    @tag("t(visual[word])")
    def toggleDirection(self):
        view=self.app.stateman.view()
        visualizer=self.getAgent(view=view)
        if visualizer:
            visualizer.go(view, kind='toggle')
