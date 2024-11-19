from plug import Plug

class FitzWordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_blocker=None
        if self.app.running:
            self.addToVisualizer()
        else:
            self.app.appSoonStarts.connect(
                    self.addToVisualizer)

    def addToVisualizer(self):
        visualizer=self.app.plugman.getPlug(
                'WordVisual')
        blocker=self.app.plugman.getPlug(
                'FitzBlockWord')
        selector=self.app.plugman.getPlug(
                'Selection')
        if visualizer and blocker and selector:
            self.m_blocker=blocker
            visualizer.addVisualizer(
                    'FitzView', self)

    def visualize(self, view):
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if not selection:
            hinter=self.app.plugman.getPlug('WordHint')
            if hinter:
                self.app.stateman.toggleSubmode()
                hinter.toggleHint()
                hinter.setExitSubmode('word')

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
                item = selection.value('item')
                element = item.element()
                self.m_blocker.update(element, kind, selection)
                item.refresh()

    def toggleDirection(self, view):
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if selection:
            item = selection.value("item")
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
