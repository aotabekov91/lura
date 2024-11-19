from plug import tag, Plug

from .view import ClockView
from .overlay import ClockOverlay

class OverlayClock(Plug):

    def setup(self):
        super().setup()
        self.setupView()

    def setupView(self):
        overlay=ClockOverlay(
                app=self.app,
                view=self.app.view,
                )
        self.clock = ClockView(
            app=self.app,
            parent=overlay,
            manager=overlay,
            objectName='OverlayClock',
            )

    @tag(["<c-c>t(normal)", "<c-[>/<escape>(normal)[ClockView]"])
    def toggle(self):
        self.clock.updatePosition()
        self.clock.toggle()
