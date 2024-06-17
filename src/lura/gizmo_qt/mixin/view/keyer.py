from lura.gizmo.utils import tag


class AppKeyer:
    hasKeyer = True
    finishKeyer = "<c-!>"
    keyerTarget = None
    keyerActivated = False

    @tag("gA(normal)")
    def setAppKeyer(self, xrange=None, **kwargs):
        if not type(xrange) == int:
            return
        if not self.checkProp("hasServer", self.app):
            return
        idx = self.app.ui.posIndex()
        if idx == xrange:
            self.octivateKeyer()
        else:
            self.keyerTarget = xrange
            self.app.earman.setKeyer(self.appKeyer)

    def octivateKeyer(self):
        raise
        self.keyerTarget = None
        self.app.earman.setKeyer()

    def checkKeyerFinish(self, e):
        p = self.app.earman.getPressed(e)
        t = self.app.earman.getText(p)
        if p and e.text():
            if t == self.finishKeyer:
                self.octivateKeyer()
                return True
        return False

    def appKeyer(self, e):
        if not self.checkKeyerFinish(e):
            d = self.app.earman.encodeInput(e)
            d["source"] = self.app.ui.posIndex()
            req = {
                "data": d,
                "object": "app.ui",
                "action": "actOnAppKeyer",
                "target": self.keyerTarget,
            }
            return self.app.server.request(**req)

    def actOnAppKeyer(self, *args, **kwargs):
        e = self.app.earman.decodeInput(*args, **kwargs)
        self.app.earman.handleEvent(e)
