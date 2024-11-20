from plug import Plug, tag

class InputMode(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, annotator):
        self.m_agents[name]=annotator

    def getAgent(self, name=None, model=None):
        if model and not name:
            name=model.__class__.__name__
        return self.m_agents.get(name, None)
