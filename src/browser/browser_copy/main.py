from plug import Plug

class BrowserCopy(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        if self.app:
            self.app.buffman.addCopier('BrowserView', self)

    def activate(self, view, **kwargs):
        if view:
            copy = self.app.buffman.create(
                    view.__class__, 
                    config=view.config(),
                    )
            copy.setModel(view.model())
            copy.setManager(view.manager())
            zoom=self.app.delegman.delegate(
                    'normal', None, view, 'zoomState')
            if zoom:
                self.app.delegman.delegate(
                        'normal', None, view, 'zoom', **zoom)
            goTo=self.app.delegman.delegate(
                    'normal', None, view, 'goToState')
            if goTo:
                self.app.delegman.delegate(
                        'normal', None, view, 'goTo', **goTo)
            return copy
