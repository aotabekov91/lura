from plug import tag, Plug

from .view import Clock

class OverlayClock(Plug):

    def setup(self):
        super().setup()
        self.clock = Clock(
            parent=self.app.view.overlay,
            app=self.app,
            manager=self.app.view.overlay,
            objectName="OverlayClock")

    @tag(["<c-c>t(normal)", "<c-[>/<escape>(normal)[Clock]"])
    def toggle(self):
        self.clock.updatePosition()
        self.clock.toggle()
