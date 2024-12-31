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
            normal=self.app.plugman.getPlug('Normal')
            copy.setModel(view.model())
            copy.setManager(view.manager())
            if normal:
                zoom=normal.currentZoom(view=view)
                position=normal.currentPosition(view=view)
                normal.activate(action='goTo', view=copy, **position)
                normal.activate(action='zoom', view=copy, **zoom)
            return copy
