from plug import Plug, tag

class WordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_visualizers={}

    def addVisualizer(self, name, visualizer):
        self.m_visualizers[name]=visualizer

    def visualizer(self, name):
        return self.m_visualizers.get(name, None)

    @tag(["<c-w>(visual)", "<c-w>/<c-[>(visual[word])"])
    def toggleWordVisual(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            submode=self.app.stateman.toggleSubmode(
                    "word")
            if submode=='word':
                if self.check('visualize', visualizer):
                    visualizer.visualize(view)
            else:
                if self.check('unvisualize', visualizer):
                    visualizer.unvisualize(view)

    @tag("<c-j>(visual[word])")
    def jump(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(view, kind='jump')

    @tag("o(visual[word])]")
    def goFirst(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='first')

    @tag("$(visual[word])")
    def goLast(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='last')

    @tag("k(visual[word])")
    def goUp(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='up')

    @tag("j(visual[word])")
    def goDown(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='down')

    @tag("l(visual[word])")
    def goLeft(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='right')

    @tag("h(visual[word])")
    def goRight(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(
                    view, xrange=xrange, kind='left')

    @tag("t(visual[word])")
    def toggleDirection(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        visualizer=self.visualizer(name)
        if visualizer:
            visualizer.go(view, kind='toggle')
