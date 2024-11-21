from plug import Plug, tag

class InputMode(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, annotator):
        self.m_agents[name]=annotator

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag('<escape>/<c-[>(insert)')
    def octivate(self):
        self.app.stateman.activate('normal')

    @tag('i(normal)')
    def insert(self, view=None, xrange=[1], **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            self.app.stateman.activate('insert')
            agent.activate(
                    view=view, 
                    xrange=xrange, 
                    kind='insert',
                    **kwargs
                    )

    @tag('a(normal)')
    def append(self, view=None, xrange=[1], **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        if agent:
            self.app.stateman.activate('insert')
            agent.activate(
                    view=view, 
                    xrange=xrange, 
                    kind='append',
                    **kwargs
                    )
