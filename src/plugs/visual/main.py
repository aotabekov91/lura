from plug import Plug, tag

class Visual(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name):
        return self.m_agents.get(name, None)

    @tag('<c-v>(normal)')
    def activate(self, submode=None, **kwargs):
        super().activate()
        if self.getAgent(name=submode):
            self.app.stateman.activate(
                    moder=self,
                    mode='visual',
                    submode=submode,
                    **kwargs)
        else:
            self.app.stateman.activate(
                    moder=self,
                    mode='visual', 
                    **kwargs)

    @tag('<c-v>/<escape>(visual[any])')
    def octivate(self, **kwargs):
        submoder=self.app.stateman.submoder()
        if submoder:
            submoder.octivate(**kwargs)
        self.app.stateman.activate()
