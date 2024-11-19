from plug import Plug

class FitzCopy(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToCopier()
        else:
            self.app.appSoonStarts.connect(
                    self.addToCopier)

    def addToCopier(self):
        copier=self.app.plugman.getPlug('Copy')
        if copier:
            copier.addCopier('FitzView', self)

    def copy(self, view):
        zoom=None
        position=None
        zoomer=self.app.plugman.getPlug('Zoom')
        if zoomer:
            zoom=zoomer.currentZoom(view=view)
        goer=self.app.plugman.getPlug('Go')
        if goer:
            position=goer.currentPosition(view=view)
        manager = view.manager()
        klass = view.__class__
        copy = self.app.buffman.create(
            klass,
            app=self.app,
            config=view.config())
        copy.setModel(view.model())
        self.app.buffman.saveView(view.model(), copy)
        copy.setManager(manager)
        if zoom:
            zoomer.zoomTo(view=copy, **zoom)
        if position:
            goer.goTo(view=copy, **position)
        return copy
