from plug import Plug, tag

class BoxHint(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if name is None and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag(["<c-b>(hint)", "<c-b>/<c-[>(hint[box])"])
    def toggle(self, xrange=[1]):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            submode = self.app.stateman.setSubmode(
                    submode="box", toggle_submode=True)
            if submode == "box":
                agent.activate(view, xrange=xrange)
            else:
                agent.octivate(view, xrange=xrange)

    @tag("<c-i>(hint[box])")
    def increment(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.getAgent(name)
        hinter.increment(view, xrange=xrange)

    @tag("<c-d>(hint[box])")
    def decrement(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.getAgent(name)
        hinter.decrement(view, xrange=xrange)
