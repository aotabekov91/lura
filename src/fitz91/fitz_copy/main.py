from plug import Plug

class FitzCopy(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        if self.app:
            self.app.buffman.addCopier('FitzView', self)

    def activate(self, view, **kwargs):
        zoom=None
        position=None
        zoomer=self.app.plugman.getPlug('Zoom')
        if zoomer:
            zoom=zoomer.currentZoom(view=view)
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            position=normal.currentPosition(view=view)
        manager = view.manager()
        klass = view.__class__
        copy = self.app.buffman.create(
            klass,
            app=self.app,
            config=view.config())
        copy.setModel(view.model())
        copy.setManager(manager)
        if zoom:
            zoomer.zoomTo(view=copy, **zoom)
        if position:
            normal.activate(action='goTo', view=copy, **position)
        return copy
