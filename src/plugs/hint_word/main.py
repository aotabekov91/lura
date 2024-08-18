from plug import Plug, tag

class WordHint(Plug):

    def setup(self):
        super().setup()
        self.m_hinters={}
        self.m_submode=None

    def setExitSubmode(self, submode=None):
        self.m_submode=submode

    def addHinter(self, name, hinter):
        self.m_hinters[name]=hinter

    def hinter(self, name):
        return self.m_hinters.get(name, None)

    @tag(["<c-w>(hint)", "<c-w>/<c-[>(hint[word])"])
    def toggleHint(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.hinter(name)
        if hinter:
            submode=self.app.stateman.toggleSubmode(
                    submode='word')
            if submode=='word':
                hinter.hint(view)
            else:
                hinter.unhint(view)
                if self.m_submode:
                    self.app.stateman.toggleSubmode(
                            submode=self.m_submode)

