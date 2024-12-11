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
        # selector=self.app.plugman.getPlug('Selection')
        # selection=selector.selection(view=view)
        if agent:# and selection:
            self.app.stateman.setSubmode(
                    submode="band", toggle_submode=True)

    def activate(self, view=None, **kwargs):
        if view is None:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.activate(view=view, **kwargs)

    def octivate(self, view=None, **kwargs):
        raise

    @tag("G(visual[band])")
    def setCorner(self, xrange=None, **kwargs):
        self.activate(action='goTo', kind='corner', xrange=xrange, **kwargs)

    @tag("l(visual[band])")
    def right(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind='right', xrange=xrange, **kwargs)

    @tag("h(visual[band])")
    def left(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind='left', xrange=xrange, **kwargs)

    @tag("k(visual[band])")
    def up(self, xrange=[1], **kwargs): 
        self.activate(action='goTo', kind='up', xrange=xrange, **kwargs)

    @tag("j(visual[band])")
    def down(self, xrange=[1], **kwargs):
        self.activate(action='goTo', kind='down', xrange=xrange, **kwargs)
