from plug import tag, Plug

from .utils import Node

class Leaper(Plug):

    node_class = Node

    def setup(self):
        super().setup()
        self.m_leaps={}
        if self.app.running:
            self.connectLeaper()
        else:
            self.app.appIsLaunched.connect(
                    self.connectLeaper)
        self.app.buffman.viewCreated.connect(
                self.saveView)

    def connectLeaper(self, kind='connect'):
        normal=self.app.plugman.getPlug('Normal')
        if normal and kind=='connect':
            normal.stateChanged.connect(self.setNode)
        elif normal and kind=='disconnect':
            normal.stateChanged.disconnect(self.setNode)

    def saveView(self, view):
        functor=self.app.delegman.getAgent(
                'normal', None, view, 'goTo')
        if functor:
            node=self.createNode()
            self.saveNode(view, node)

    def setNode(self, state, view, data):
        if state=='goTo' and view in self.m_leaps:
            node=self.getNode(view)
            if node.data!=data:
                current=self.createNode(
                        precedent=node, data=data)
                node.ascendent = current 
                self.saveNode(view, current)

    def getNode(self, view):
        return self.m_leaps.get(view, None)

    def saveNode(self, view, node):
        self.m_leaps[view]=node

    def createNode(self, *args, **kwargs):
        return self.node_class(*args, **kwargs)

    @tag('<c-i>(normal)')
    def next(self, view=None, xrange=[1], **kwargs):
        if not view:
            view=self.app.stateman.view()
        node=self.getNode(view)
        if node:
            self.connectLeaper('disconnect')
            self.activate(
                    view=view,
                    node=node,
                    kind='next',
                    xrange=xrange)
            self.connectLeaper()

    @tag('<c-o>(normal)')
    def prev(self, view=None, xrange=[1], **kwargs):
        if not view:
            view=self.app.stateman.view()
        node=self.getNode(view)
        if node:
            self.connectLeaper('disconnect')
            self.activate(
                    view=view,
                    node=node,
                    kind='prev',
                    xrange=xrange)
            self.connectLeaper()

    def activate(
            self, 
            view, 
            kind=None, 
            node=None, 
            xrange=[1], 
            ):
        for i in range(xrange[-1]):
            node = self.getNode(view)
            if kind == "next":
                ascendent=node.ascendent
                if not ascendent:
                    break
                data=ascendent.data
                self.saveNode(view, ascendent)
                self.app.delegman.delegate(
                        mode='normal',
                        action='goTo', 
                        view=view, 
                        data=data)
            elif kind == "prev":
                precedent=node.precedent
                if not precedent:
                    break
                data=precedent.data
                if not data:
                    break
                self.saveNode(view, precedent)
                self.app.delegman.delegate(
                        mode='normal',
                        action='goTo', 
                        view=view, 
                        data=data)
