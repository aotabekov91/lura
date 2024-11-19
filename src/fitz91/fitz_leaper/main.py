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
        goer=self.app.plugman.getPlug('FitzGo')
        leaper=self.app.plugman.getPlug('Leaper')
        if leaper and goer:
            leaper.addAgent('FitzView', self)

    def go(self, view, kind=None, node=None, xrange=[1], leaper=None):
        goer=self.app.plugman.getPlug('FitzGo')
        for i in range(xrange[-1]):
            node = leaper.getNode(view)
            if kind == "next":
                ascendent=node.ascendent
                if not ascendent:
                    break
                data=ascendent.data
                leaper.saveNode(view, ascendent)
                goer.goTo(view=view, **data)
            elif kind == "prev":
                precedent=node.precedent
                if not precedent:
                    break
                data=precedent.data
                if not data:
                    break
                leaper.saveNode(view, precedent)
                goer.goTo(view=view, **data)
