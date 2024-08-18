from plug import Plug

class FitzLeaper(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToLeaper()
        else:
            self.app.appSoonStarts.connect(
                    self.addToLeaper)

    def addToLeaper(self):
        self.leaper=self.app.plugman.plugs.get('Leaper')
        if self.leaper:
            self.leaper.addLeaper('FitzView', self)
            self.app.buffman.viewCreated.connect(
                    self.createNode)
            self.app.buffman.viewCreated.connect(
                    self.connectView)

    def createNode(self, view):
        if view.__class__.__name__=='FitzView':
            node=self.leaper.createNode()
            self.leaper.saveNode(view, node)

    def connectView(self, view, kind="connect"):
        if view.__class__.__name__=='FitzView':
            if kind == "connect":
                view.positionJumped.connect(
                        self.setNode)
                view.positionToBeJumped.connect(
                        self.updateNode)
            else:
                view.positionJumped.disconnect(
                        self.setNode)
                view.positionToBeJumped.disconnect(
                        self.updateNode)

    def go(self, view, kind=None, node=None, xrange=[1]):
        self.connectView(view, "disconnect")
        for _ in range(xrange[-1]):
            node = self.leaper.node(view)
            if kind == "next":
                ascendent=node.ascendent
                if not ascendent:
                    break
                data=ascendent.data
                self.leaper.saveNode(view, ascendent)
                view.openLocator(data=data, kind="position")
            elif kind == "prev":
                precedent=node.precedent
                if not precedent:
                    break
                data=precedent.data
                if not data:
                    break
                self.leaper.saveNode(view, precedent)
                view.openLocator(data=data, kind="position")
        self.connectView(view)

    def setNode(self, view, position):
        node=self.leaper.node(view)
        if node.data!=position:
            current=self.leaper.createNode(
                    precedent=node, data=position)
            node.ascendent = current 
            self.leaper.saveNode(view, current)

    def updateNode(self, view, position):
        node=self.leaper.node(view)
        if not node.data:
            node.data=position
