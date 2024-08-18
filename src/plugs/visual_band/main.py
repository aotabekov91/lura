from plug import tag, Plug

class BandVisual(Plug):

    def setup(self):
        super().setup()
        self.m_bander={}

    def addVisualizer(self, name, bander):
        self.m_bander[name]=bander

    def visualizer(self, name):
        return self.m_bander.get(name, None)

    @tag(["<c-b>(visual)", "<c-b>/<c-[>(visual[band])"])
    def toggle(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bander=self.visualizer(name)
        if bander:
            submode = self.app.stateman.toggleSubmode("band")
            if submode == "band":
                bander.activate(view)
            else:
                bander.octivate(view)

    @tag("G(visual[band])")
    def setCorner(self, xrange=None):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bander=self.visualizer(name)
        if bander:
            bander.go(
                    view, 
                    kind='corner', 
                    xrange=xrange)

    @tag("l(visual[band])")
    def right(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bander=self.visualizer(name)
        if bander:
            bander.go(
                    view,
                    kind='right',
                    xrange=xrange)

    @tag("h(visual[band])")
    def left(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bander=self.visualizer(name)
        if bander:
            bander.go(
                    view,
                    kind='left',
                    xrange=xrange)

    @tag("k(visual[band])")
    def up(self, xrange=[1]): 
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bander=self.visualizer(name)
        if bander:
            bander.go(
                    view,
                    kind='up',
                    xrange=xrange)

    @tag("j(visual[band])")
    def down(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bander=self.visualizer(name)
        if bander:
            bander.go(
                    view,
                    kind='down',
                    xrange=xrange)
