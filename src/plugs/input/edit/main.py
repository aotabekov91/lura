from plug import Plug, tag

class Edit(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, action, kind, name):
        if not action in self.m_agents:
            self.m_agents[action]={}
        self.m_agents[action][kind]=name

    def getAgent(self, action, name=None, view=None):
        data=self.m_agents.get(action, {})
        if not name and view:
            name=view.__class__.__name__
        return data.get(name, None)

    def activate(self, view=None, action=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(action=action, view=view)
        if agent:
            self.app.stateman.setSubmode(action)
            agent.activate(view=view, action=action, **kwargs)
        
    @tag(['<c-e>(normal/edit)', '<escape>/<c-[>(edit)'])
    def toggle(self, **kwargs):
        self.app.stateman.toggle('edit')

    @tag('i(edit)')
    def insert(self, xrange=[1], **kwargs):
        self.activate(action='insert', xrange=xrange, **kwargs)

    @tag('a(edit)')
    def append(self, view=None, xrange=[1], **kwargs):
        self.activate(action='apped', xrange=xrange, **kwargs)
