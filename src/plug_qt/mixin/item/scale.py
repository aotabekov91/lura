class Scale:
    canZoom = True
    roundScale = 3

    def setup(self):
        super().setup()
        self.viewIsSet.connect(self.connectToScaleChanges)

    def connectToScaleChanges(self):
        v = self.m_view
        if not v:
            return
        v.scaleModeChanged.connect(self.updateScaleMode)

    def updateScaleMode(self, m, v=None):
        scale = self.calculateScale(m)
        self.setScaleMode(scale)

    def calculateScale(self, m):
        if not m:
            return self.scale
        if not self.m_view:
            return
        s = self.m_view.size()
        w, h = s.width(), s.height()
        dw, dh = self.displayedSize()
        if m == "width":
            scale = w / float(dw)
        elif m == "height":
            scale = h / float(dh)
        elif m == "adjust":
            scale = min(w / float(dw), h / float(dh))
        else:
            scale = float(m) * float(self.scale)
        return scale

    def setScaleMode(self, scale):
        scale = round(scale, self.roundScale)
        self.scale = scale
        self.redraw()
