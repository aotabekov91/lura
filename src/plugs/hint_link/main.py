from plug import Plug, tag

class LinkHint(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, hinter):
        self.m_agents[name]=hinter

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def searchAgent(self, view=None):
        if view is None:
            view=self.app.stateman.view()
        return self.getAgent(view=view), view

    @tag(["<c-l>(hint/hint[link])", "<c-[>/<escape>(hint[link])"])
    def toggle(self, *args, **kwargs):
        super().toggle(*args, **kwargs)

    def activate(self, view=None, **kwargs):
        agent, view=self.searchAgent(view=view)
        if agent:
            super().activate()
            self.app.stateman.setSubmode(
                    submoder=self,
                    submode='link')
            agent.activate(view=view, **kwargs)

    def octivate(self, view=None, **kwargs):
        agent, view=self.searchAgent(view=view)
        if agent:
            super().octivate()
            self.app.stateman.setSubmode()
            agent.octivate(view=view, **kwargs)
