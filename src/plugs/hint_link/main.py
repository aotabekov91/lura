from plug import Plug, tag

class LinkHint(Plug):

    def setup(self):
        super().setup()
        self.m_hinters={}

    def addHinter(self, name, hinter):
        self.m_hinters[name]=hinter

    def hinter(self, name):
        return self.m_hinters.get(name, None)

    @tag("<c-l>(hint/hint[link])")
    def toggleHint(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.hinter(name)
        if hinter:
            submode=self.app.stateman.toggleSubmode(
                    submode='link')
            if submode=='link':
                hinter.hint(view)
            else:
                hinter.unhint(view)
