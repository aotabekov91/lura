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
        copier=self.app.plugman.plugs.get('Copy')
        if copier:
            copier.addCopier('FitzView', self)

    def copy(self, view):
        mode = view.scaleMode
        pos = view.getPosition()
        manager = view.manager()
        klass = view.__class__
        view_copy = self.app.buffman.create(
            klass,
            app=self.app,
            config=view.config())
        view_copy.setModel(view.model())
        self.app.buffman.saveView(view.model(), view_copy)
        view_copy.setManager(manager)
        view_copy.goTo(*pos)
        view_copy.setScaleMode(mode)
        return view_copy
