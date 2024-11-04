from plug import Plug, tag

class AnnotationHint(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, hinter):
        self.m_agents[name]=hinter

    def agent(self, name):
        return self.m_agents.get(name, None)

    @tag(["<c-a>(hint)", "<c-a>/<c-[>(hint[annotation])"])
    def toggle(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        hinter=self.agent(name)
        if hinter:
            submode=self.app.stateman.toggleSubmode(
                    submode='annotation')
            if submode=='annotation':
                hinter.activate(view)
            else:
                hinter.octivate(view)
