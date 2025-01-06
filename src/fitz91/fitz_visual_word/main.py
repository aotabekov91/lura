from plug import Plug

from .blocker import FitzBlockWord 

class FitzWordVisual(Plug):

    def setup(self):
        super().setup()
        self.m_blocker=FitzBlockWord()
        self.addAgent()

    def blocker(self):
        return self.m_blocker

    def addAgent(self):
        self.app.delegman.addAgent(
                'visual', 'word', 'FitzView', 'goTo', self.goTo)
        self.app.delegman.addAgent(
                'visual', 'word', 'FitzView', 'start', self.start)

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
        for _ in range(xrange[-1]):
            selection=self.app.delegman.delegate(
                    action='getSelection', data={'view': view})
            if selection:
                item = selection['item']
                element = item.element()
                self.m_blocker.update(element, kind, selection)
                item.refresh()

    def toggleDirection(self, view=None, **kwargs):
        selection=self.app.delegman.delegate(
                action='getSelection', data={'view': view})
        if selection:
            item = selection['item']
            element = item.element()
            element.toggleDirection(0)

    def jump(self, view=None, data=None):
        if data:
            item = data["item"]
            view=item.view()
            element = item.element()
            selection=self.app.delegman.delegate(
                    action='getSelection', data={'view': view})
            if selection and data:
                element.jumpToBlock(selection, data)
            elif data:
                data['view']=view
                selection=self.app.delegman.delegate(
                        action='setSelection', data=data)
