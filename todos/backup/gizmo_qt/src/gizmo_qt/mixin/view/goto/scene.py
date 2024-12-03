from gizmo.utils import tag

from .view import ViewGo


class SceneGo(ViewGo):

    @tag("<c-h>(normal)[^]")
    def goToScreenLeft(self, xrange=[1], **kwargs):
        self.moveScreen("left", xrange)

    @tag("<c-l>(normal)[^]")
    def goToScreenRight(self, xrange=[1], **kwargs):
        self.moveScreen("right", xrange)

    @tag("<c-space>/<c-k>(normal)[^]")
    def goToScreenUp(self, xrange=[1], **kwargs):
        self.moveScreen("up", xrange)

    @tag("<space>/<c-j>(normal)[^]")
    def goToScreenDown(self, xrange=[1], **kwargs):
        self.moveScreen("down", xrange)

    def goToNext(self, *args, **kwargs):
        self.nextItem()

    def goToPrev(self, *args, **kwargs):
        self.prevItem()

    def goToDown(self, xrange=[1], **kwargs):
        self.moveLine("down", xrange)

    def goToUp(self, xrange=[1], **kwargs):
        self.moveLine("up", xrange)

    def goToLeft(self, xrange=[1], **kwargs):
        self.moveLine("left", xrange)

    def goToRight(self, xrange=[1], **kwargs):
        self.moveLine("right", xrange)

    def goToLast(self, **kwargs):
        self.goTo(self.count())

    def moveScreen(self, kind, xrange=[1]):
        s = self.size()
        h, w = s.height(), s.width()
        # sr=self.scene().sceneRect()
        # sh, sw = sr.height(), sr.width()
        vb = self.verticalScrollBar()
        hb = self.horizontalScrollBar()
        if self.checkProp("hasLayout"):
            h = self.m_layout.height(h)
            w = self.m_layout.height(w)
        if kind == "up":
            dx = vb.value() - h * xrange[-1]
            # dx=max(0, dx)
            vb.setValue(int(dx))
        elif kind == "down":
            dx = vb.value() + h * xrange[-1]
            # dx=min(sh, dx)
            vb.setValue(int(dx))
        elif kind == "left":
            dy = hb.value() - w * xrange[-1]
            # dy=max(0, dy)
            hb.setValue(int(dy))
        elif kind == "right":
            dy = hb.value() + w * xrange[-1]
            # dy=min(sw, dy)
            hb.setValue(int(dy))
        self.setVisibleItem()
        self.positionChanged.emit()

    def moveLine(self, kind, xrange=[1]):
        s = self.size()
        h, w = s.height(), s.width()
        # sr=self.scene().sceneRect()
        vb = self.verticalScrollBar()
        hb = self.horizontalScrollBar()
        if self.checkProp("hasLayout"):
            h = self.m_layout.height(h)
            w = self.m_layout.height(w)
        # h=h*self.zoomFactor*0.5
        # w=w*self.zoomFactor*0.5
        h = h * self.zoomFactor  # *0.5
        w = w * self.zoomFactor  # *0.5
        if kind == "down":
            dx = vb.value() + h * xrange[-1]
            # dx=min(sr.height(), dx)
            vb.setValue(int(dx))
        elif kind == "up":
            dx = vb.value() - h * xrange[-1]
            # dx=max(0, dx)
            vb.setValue(int(dx))
        elif kind == "right":
            dx = hb.value() + w * xrange[-1]
            hb.setValue(int(dx))
        elif kind == "left":
            dx = hb.value() - w * xrange[-1]
            hb.setValue(int(dx))
        self.setVisibleItem()
        self.positionChanged.emit()

    def setVisibleItem(self):
        pass
