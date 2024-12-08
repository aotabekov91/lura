from plug import Plug, tag

class LinkHint(Plug):

    def setup(self):
        super().setup()
        self.m_hinters={}

    def addAgent(self, name, hinter):
        self.m_hinters[name]=hinter

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_hinters.get(name, None)

    @tag(["<c-l>(hint/hint[link])", "<c-[>/<escape>(hint[link])"])
    def toggleHint(self):
        view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            submode=self.app.stateman.activate(
                    submode='link', toggle_submode=True)
            if submode=='link':
                agent.hint(view=view)
            else:
                agent.unhint(view=view)
