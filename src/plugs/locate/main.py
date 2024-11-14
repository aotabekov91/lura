from plug import Plug, hashdict

class Locate(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, kind, name, agent):
        if not kind in self.m_agents:
            self.m_agents[kind]={}
        self.m_agents[kind][name]=agent

    def getAgent(self, kind, name=None, agent=None):
        if agent and not name:
            name=agent.__class__.__name__
        agents=self.m_agents.get(kind, {})
        return agents.get(name)

    def createLocator(self, data={}, **kwargs):
        return hashdict(data)

    def findLocator(self, locator, kind, agent):
        name = f"{kind}{locator.title()}Locator"
        func=getattr(agent, name, None)
        if func:
            return func
        locator=self.getAgent(locator, agent)
        if locator:
            return self.findLocator(locator, kind, locator)

