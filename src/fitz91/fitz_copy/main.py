from plug import Plug

class FitzCopy(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        if self.app:
            self.app.buffman.addCopier('FitzView', self)

    def activate(self, view, **kwargs):
        if view:
            copy = self.app.buffman.create(
                    view.__class__, 
                    config=view.config(),
                    )
            copy.setModel(view.model())
            copy.setManager(view.manager())
            zoom=self.app.delegman.delegate(
                    'normal', None, view=view, action='zoomState')
            if zoom:
                zoom=self.app.delegman.delegate(
                        'normal', None, view=copy, action='zoom', data=zoom)
            goTo=self.app.delegman.delegate(
                    'normal', None, view=view, action='goToState')
            if goTo:
                goTo=self.app.delegman.delegate(
                        'normal', None, view=copy, action='goTo', data=goTo)
            return copy
