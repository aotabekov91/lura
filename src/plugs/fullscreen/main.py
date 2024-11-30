from plug import Plug, tag

class Fullscreen(Plug):

    def setup(self):
        super().setup()
        self.m_fullscreen={}
        self.m_fullsreeners={}

    def addAgent(self, name, getAgent):
        self.m_fullsreeners[name]=getAgent

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        agent=self.m_fullsreeners.get(name, None)
        if agent:
            return agent
        elif view and view.manager():
            return self.getAgent(view=view.manager())

    def checkFullscreen(self, view):
        return self.m_fullscreen.get(view, False)

    def setFullscreen(self, view, cond):
        self.m_fullscreen[view]=cond

    @tag("f(normal)")
    def toggle(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        print(view, agent, self.m_fullsreeners)
        if agent:
            if not self.checkFullscreen(view):
                agent.activate(view=view, **kwargs)
                self.setFullscreen(view, True)
            else:
                agent.octivate(view=view, **kwargs)
                self.setFullscreen(view, False)
