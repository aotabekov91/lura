from plug import Plug, tag

class WordHint(Plug):

    def setup(self):
        super().setup()
        self.m_hinters={}

    def addAgent(self, name, hinter):
        self.m_hinters[name]=hinter

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_hinters.get(name, None)

    def searchAgent(self, view=None):
        if not view:
            view=self.app.stateman.view()
        return self.getAgent(view=view), view

    def activate(self, view=None, **kwargs):
        agent, view=self.searchAgent(view=view)
        if agent:
            super().activate()
            self.app.stateman.setSubmode(
                    submoder=self, submode='word')
            agent.activate(view=view, **kwargs)

    def octivate(self, view=None, **kwargs):
        agent, view=self.searchAgent(view=view)
        if agent:
            super().octivate()
            self.app.stateman.setSubmode()
            agent.octivate(view=view, **kwargs)

    @tag(["<c-w>(hint)", "<c-w>/<c-[>(hint[word])"])
    def toggle(self, **kwargs):
        super().toggle(**kwargs)
