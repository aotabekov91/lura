from plug import tag, Plug

from .view import Clock

class OverlayClock(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.setupView()
        else:
            self.app.appSoonStarts.connect(
                    self.setupView)

    def setupView(self):
        overlayer=self.app.plugman.plugs.get('Overlay')
        if overlayer:
            app_overlay=overlayer.getOverlay(
                    view=self.app.view)
            self.clock = Clock(
                app=self.app,
                parent=app_overlay,
                manager=app_overlay,
                objectName="OverlayClock")

    @tag(["<c-c>t(normal)", "<c-[>/<escape>(normal)[Clock]"])
    def toggle(self):
        self.clock.updatePosition()
        self.clock.toggle()
        view=self.app.stateman.subview()
        view.activate()
