from plug import Plug, tag

class BoxHint(Plug):

    def setup(self):
        super().setup()
        self.m_hinters={}
        self.m_submode=None

    def addHinter(self, name, hinter):
        self.m_hinters[name]=hinter

    def hinter(self, name):
        return self.m_hinters.get(name, None)

    def setExitSubmode(self, submode=None):
        self.m_submode=submode

    def exitSubmode(self):
        return self.m_submode

    @tag(["<c-b>(hint)", "<c-b>/<c-[>(hint[box])"])
    def toggle(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.hinter(name)
        if hinter:
            submode = self.app.stateman.activate(
                    submode="box", toggle_submode=True)
            if submode == "box":
                hinter.activate(view, xrange=xrange)
            else:
                hinter.octivate(view, xrange=xrange)
                submode=self.exitSubmode()
                if submode:
                    self.app.stateman.setSubmode(submode)
                self.setExitSubmode()

    @tag("<c-i>(hint[box])")
    def increment(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.hinter(name)
        hinter.increment(view, xrange=xrange)

    @tag("<c-d>(hint[box])")
    def decrement(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.hinter(name)
        hinter.decrement(view, xrange=xrange)
