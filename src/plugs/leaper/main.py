from plug import tag, Plug

class Node:
    def __init__(
            self, 
            data=None, 
            ascendent=None, 
            precedent=None
            ):
        self.data = data
        self.ascendent = ascendent
        self.precedent = precedent

class Leaper(Plug):

    node_class = Node

    def setup(self):
        super().setup()
        self.m_leaps={}
        self.m_agents={}
        self.app.buffman.viewCreated.connect(
                self.saveView)

    def addAgent(self, name, leaper):
        self.m_agents[name]=leaper

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def saveView(self, view):
        agent=self.getAgent(view=view)
        if agent:
            node=self.createNode()
            self.saveNode(view, node)
            self.connectView(view)

    def connectView(self, view, kind="connect"):
        go=self.app.plugman.getPlug('Go')
        goer=go.getAgent(view=view)
        if goer and kind == "connect":
            go.positionChanged.connect(
                    self.setNode)
        elif goer and kind == "disconnect":
            go.positionChanged.disconnect(
                    self.setNode)

    def setNode(self, view, data):
        node=self.getNode(view)
        if node.data!=data:
            current=self.createNode(
                    precedent=node, data=data)
            node.ascendent = current 
            self.saveNode(view, current)

    def getNode(self, view):
        return self.m_leaps.get(view)

    def saveNode(self, view, node):
        self.m_leaps[view]=node

    def createNode(self, *args, **kwargs):
        return self.node_class(*args, **kwargs)

    @tag('<c-I>(normal)')
    def next(self, xrange=[1]):
        view=self.app.stateman.view()
        leaper=self.getAgent(view=view)
        if leaper:
            node=self.getNode(view)
            self.connectView(view, kind='disconnect')
            leaper.go(
                    view=view,
                    node=node,
                    kind='next',
                    leaper=self,
                    xrange=xrange,
                    )
            self.connectView(view)

    @tag('<c-O>(normal)')
    def prev(self, xrange=[1]):
        view=self.app.stateman.view()
        leaper=self.getAgent(view=view)
        if leaper:
            node=self.getNode(view)
            self.connectView(view, kind='disconnect')
            leaper.go(
                    view=view,
                    node=node,
                    kind='prev',
                    leaper=self,
                    xrange=xrange,
                    )
            self.connectView(view)
