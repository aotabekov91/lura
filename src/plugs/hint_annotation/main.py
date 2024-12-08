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
        agent=self.agent(view=view)
        if agent:
            self.app.stateman.setSubmode(
                    submode='annotation', toggle_submode=True)
            agent.activate(view=view)

    @tag("<c-a>/<c-[>(hint[annotation])")
    def octivate(self):
        view=self.app.stateman.view()
        agent=self.agent(view=view)
        if agent:
            agent.octivate(view=view)
            self.app.stateman.activate()
