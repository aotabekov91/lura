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
        self.m_leapers={}

    def addLeaper(self, name, leaper):
        self.m_leapers[name]=leaper

    def leaper(self, name):
        return self.m_leapers.get(name, None)

    def node(self, view):
        return self.m_leaps.get(view)

    def saveNode(self, view, node):
        self.m_leaps[view]=node

    def createNode(self, *args, **kwargs):
        return self.node_class(*args, **kwargs)

    @tag('i(normal)')
    def next(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        leaper=self.leaper(name)
        if leaper:
            node=self.node(view)
            leaper.go(
                    view=view,
                    node=node,
                    kind='next',
                    xrange=xrange)

    @tag('o(normal)')
    def prev(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        leaper=self.leaper(name)
        if leaper:
            node=self.node(view)
            leaper.go(
                    view=view,
                    node=node,
                    kind='prev',
                    xrange=xrange)
