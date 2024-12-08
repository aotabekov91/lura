from plug import Plug, tag

class WordHint(Plug):

    def setup(self):
        super().setup()
        self.m_hinters={}

    def setExitSubmode(self, submode=None):
        self.m_submode=submode

    def addAgent(self, name, hinter):
        self.m_hinters[name]=hinter

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_hinters.get(name, None)

    @tag(["<c-w>(hint)", "<c-w>/<c-[>(hint[word])"])
    def toggle(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        hinter=self.getAgent(view=view)
        if hinter:
            self.app.stateman.setSubmode(
                    submode='word', toggle_submode=True)
            submode=self.app.stateman.submode()
            if submode=='word':
                self.activate(view=view, **kwargs)
            else:
                self.octivate(view=view, **kwargs)

    def activate(self, view=None, **kwargs):
        if not view:
            self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.activate(view=view, **kwargs)

    def octivate(self, view=None, **kwargs):
        if not view:
            self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            agent.octivate(view=view, **kwargs)
        self.app.stateman.activate()
