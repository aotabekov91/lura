from plug import Plug

class FitzWordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_blocker=None
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        handler=self.app.plugman.getPlug(
                'WordVisual')
        blocker=self.app.plugman.getPlug(
                'FitzBlockWord')
        selector=self.app.plugman.getPlug(
                'Selection')
        if handler and blocker and selector:
            self.m_blocker=blocker
            handler.addAgent('FitzView', self)

    def unvisualize(self, view=None, **kwargs):
        pass

    def visualize(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        hinter=self.app.plugman.getPlug('WordHint')
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if not selection and hinter:
            self.app.stateman.toggle('hint')
            hinter.toggle(view=view, **kwargs)

    def go(self, view, xrange=[1], kind='last'):
        selector=self.app.plugman.getPlug('Selection')
        if kind=='toggle':
            self.toggleDirection(view)
        elif kind=='jump':
            raise
        else:
            if not self.m_blocker:
                return
            for time in range(xrange[-1]):
                selection=selector.selection(view)
                if not selection:
                    return
                item = selection['item']
                element = item.element()
                self.m_blocker.update(element, kind, selection)
                item.refresh()

    def toggleDirection(self, view):
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if selection:
            item = selection['item']
            element = item.element()
            element.toggleDirection(0)

    def jump(self, kind, data):
        item = data["item"]
        view=item.view()
        element = item.element()
        block = self.selection()
        if block and data:
            element.jumpToBlock(block, data)
        elif data:
            selector=self.app.plugman.getPlug('Selection')
            selector.select(view, **data)
