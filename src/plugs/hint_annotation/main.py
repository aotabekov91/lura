from plug import Plug, tag

class AnnotationHint(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, hinter):
        self.m_agents[name]=hinter

    def agent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag("<c-a>(hint)")
    def activate(self):
        view=self.app.stateman.view()
        hinter=self.agent(view=view)
        if hinter:
            self.app.stateman.activate(
                    submode='annotation', toggle_submode=True)
            hinter.activate(view)

    @tag("<c-a>/<c-[>(hint[annotation])")
    def octivate(self):
        view=self.app.stateman.view()
        hinter=self.agent(view=view)
        if hinter:
            hinter.octivate(view)
            self.app.stateman.activate()
