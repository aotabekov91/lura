from plug import tag, Plug

class BandVisual(Plug):

    def setup(self):
        super().setup()
        self.m_agent={}

    def addAgent(self, name, agent):
        self.m_agent[name]=agent

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agent.get(name, None)

    @tag(["<c-b>(visual)", "<c-b>/<c-[>(visual[band])"])
    def toggle(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            submode = self.app.stateman.setSubmode(
                    submode="band", toggle_submode=True)
            if submode == "band":
                agent.activate(view=view, **kwargs)
            else:
                agent.octivate(view=view, **kwargs)

    @tag("G(visual[band])")
    def setCorner(self, xrange=None):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.activate(action='goTo', view=view, kind='corner', xrange=xrange)

    @tag("l(visual[band])")
    def right(self, xrange=[1]):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.go(view=view, kind='right', xrange=xrange)

    @tag("h(visual[band])")
    def left(self, xrange=[1]):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.go(view=view, kind='left', xrange=xrange)

    @tag("k(visual[band])")
    def up(self, xrange=[1]): 
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.go(view=view, kind='up', xrange=xrange)

    @tag("j(visual[band])")
    def down(self, xrange=[1]):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.go(view=view, kind='down', xrange=xrange)
