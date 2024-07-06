from PyQt6 import QtCore

from app.utils import tag


class Scale:
    canScale = True
    scaleMode = None
    zoomFactor = 0.05
    scaleModeChanged = QtCore.pyqtSignal(object, object)

    def setup(self):
        super().setup()
        self.m_zoom_scale = 1
        self.m_zoom_factor = 1
        self.scaleModeChanged.connect(self.saveScaleState)

        if self.checkProp("canFullscreen"):
            self.fullscreenToggled.connect(
                self.adjustScaleModeToFullscreen
            )

    def adjustScaleModeToFullscreen(self, cond):
        if self.scaleMode in ["width", "height"]:
            self.scale(kind=self.scaleMode)

    def saveScaleState(self):
        if self.checkProp("hasStates", self.m_model):
            p = self.getScaleLocator()
            p["state"] = "scale"
            p["value"] = self.scaleMode
            self.m_model.addState(p)

    def getScaleLocator(self, data={}, **kwargs):
        data["scaleMode"] = self.scaleMode
        return self.getLocator(
            data=data, kind="uniq", **kwargs
        )

    def setScaleLocator(self, data, initial=True, **kwargs):
        s = data.get("scale")
        self.setScaleMode(s)

    @tag("zi(normal)[^]")
    def zoomIn(self, xrange=[1,]):
        self.scale(kind="in", xrange=xrange)

    @tag("zo(normal)[^]")
    def zoomOut(self, xrange=[1,]):
        self.scale(kind="out", xrange=xrange)

    @tag("zw(normal)[^]")
    def zoomToWidth(self):
        self.scale(kind="width")

    @tag("za(normal)[^]")
    def zoomToAdjust(self):
        self.scale(kind="adjust")

    @tag("zh(normal)[^]")
    def zoomToHeight(self):
        self.scale(kind="height")

    def updateFit(self):
        adj = ["width", "height", "adjust"]
        if self.scaleMode in adj:
            self.setScaleMode(self.scaleMode)

    def setParent(self, p):
        if self.parent():
            self.reconnect("disconnect")
        super().setParent(p)
        if self.parent():
            self.reconnect()

    def reconnect(self, kind="connect"):
        p = self.parent()
        g = getattr(p, "geometryChanged", None)
        if not g:
            return
        c = getattr(g, kind)
        c(self.updateFit)

    def scale(self, kind, xrange=[1,], *args, **kwargs):
        sf = self.zoomFactor
        if len(xrange)<1: return
        if kind == "out":
            kind = (1.0 - sf) ** xrange[0]
        elif kind == "in":
            kind = (1.0 + sf) ** xrange[0]
        self.setScaleMode(kind)

    def setScaleMode(self, kind):
        self.scaleMode = kind
        self.scaleModeChanged.emit(kind, self)
        self.redraw()
