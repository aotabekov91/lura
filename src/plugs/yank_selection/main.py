from plug import Plug, tag

class YankSelection(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, yanker):
        self.m_agents[name]=yanker

    def getAgent(self, name):
        return self.m_agents.get(name, None)

    @tag(["y(yank)", "y(visual)"])
    def yankSelection(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        yanker=self.getAgent(name)
        if yanker:
            yanker.yank(view)
