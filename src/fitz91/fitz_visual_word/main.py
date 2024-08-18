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
        visualizer=self.app.plugman.plugs.get(
                'WordVisual')
        blocker=self.app.plugman.plugs.get(
                'FitzBlockWord')
        if visualizer and blocker:
            self.m_blocker=blocker
            visualizer.addVisualizer(
                    'FitzView', self)

    def visualize(self, view):
        selection=view.selection()
        if not selection:
            hinter=self.app.plugman.plugs.get('WordHint')
            if hinter:
                self.app.stateman.toggleSubmode()
                hinter.toggleHint()
                hinter.setExitSubmode('word')

    def go(self, view, xrange=[1], kind='last'):
        if kind=='toggle':
            self.toggleDirection(view)
        elif kind=='jump':
            raise
        else:
            if not self.m_blocker:
                return
            for item in range(xrange[-1]):
                selection = view.selection()
                if not selection:
                    return
                item = selection["item"]
                element = item.element()
                self.m_blocker.update(element, kind, selection)
                item.refresh()

    def toggleDirection(self, view):
        selection = view.selection()
        if selection:
            item = selection["item"]
            element = item.element()
            element.toggleDirection(0)

    def jump(self, kind, sel):
        item = sel["item"]
        element = item.element()
        s = self.selection()
        if s and sel:
            element.jumpToBlock(s, sel)
        elif sel:
            item = sel["item"]
            view.select(item, sel)
