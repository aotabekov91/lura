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
        normal=self.app.plugman.getPlug('Normal')
        leaper=self.app.plugman.getPlug('Leaper')
        if leaper and normal:
            leaper.addAgent('FitzView', self)

    def go(self, view, kind=None, node=None, xrange=[1], leaper=None):
        normal=self.app.plugman.getPlug('Normal')
        for i in range(xrange[-1]):
            node = leaper.getNode(view)
            if kind == "next":
                ascendent=node.ascendent
                if not ascendent:
                    break
                data=ascendent.data
                leaper.saveNode(view, ascendent)
                normal.activate(action='goTo', view=view, **data)
            elif kind == "prev":
                precedent=node.precedent
                if not precedent:
                    break
                data=precedent.data
                if not data:
                    break
                leaper.saveNode(view, precedent)
                normal.activate(action='goTo', view=view, **data)
