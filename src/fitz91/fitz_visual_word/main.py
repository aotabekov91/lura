from plug import Plug

from .blocker import FitzBlockWord 

class FitzWordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_blocker=FitzBlockWord()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def blocker(self):
        return self.m_blocker

    def addAgent(self):
        handler=self.app.plugman.getPlug('WordVisual')
        selector=self.app.plugman.getPlug('Selection')
        if handler and selector:
            handler.addAgent('goTo', 'FitzView', self)
            handler.addAgent('start', 'FitzView', self)

    def delegate(self, action=None, **kwargs):
        if action:
            func=getattr(self, action, None)
            if func:
                func(**kwargs)

    def start(self, view=None, **kwargs):
        print('start')
        # todo: if no selection, start hinting

    def goTo(self, kind='last', **kwargs):
        if kind=='toggle':
            self.toggleDirection(**kwargs)
        elif kind=='jump':
            raise
        else:
            self.updateBlock(kind=kind, **kwargs)

    def updateBlock(self, kind=None, view=None, xrange=[1], **kwargs):
        selector=self.app.plugman.getPlug('Selection')
        for _ in range(xrange[-1]):
            selection=selector.selection(view)
            if selection:
                item = selection['item']
                element = item.element()
                self.m_blocker.update(element, kind, selection)
                item.refresh()

    def toggleDirection(self, view=None, **kwargs):
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if selection:
            item = selection['item']
            element = item.element()
            element.toggleDirection(0)

    def jump(self, view=None, data=None):
        if data:
            item = data["item"]
            view=item.view()
            element = item.element()
            selector=self.app.plugman.getPlug('Selection')
            selection=selector.selection(view)
            if selection and data:
                element.jumpToBlock(selection, data)
            elif data:
                selector=self.app.plugman.getPlug('Selection')
                selector.select(view, **data)
