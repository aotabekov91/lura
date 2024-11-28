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
            submode=self.app.stateman.toggleSubmode(
                    submode='word')
            if submode=='word':
                self.activate(view=view, **kwargs)
            else:
                self.deactivate(view=view, **kwargs)

    def activate(self, view=None, **kwargs):
        if not view:
            self.app.stateman.view()
        hinter=self.getAgent(view=view)
        if hinter:
            hinter.hint(view=view, **kwargs)

    def deactivate(self, view=None, **kwargs):
        if not view:
            self.app.stateman.view()
        hinter=self.getAgent(view=view)
        if hinter:
            hinter.unhint(view=view, **kwargs)
        self.app.stateman.toggle()
