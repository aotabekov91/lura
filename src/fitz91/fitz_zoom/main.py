from plug import Plug

class FitzZoom(Plug):

    zoom_round=3
    zoom_factor = 0.05

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)
        self.app.buffman.viewCreated.connect(
                self.connectView)

    def addAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            normal.addAgent('zoom', 'FitzView', self)

    def connectView(self, view):
        if view and view.__class__.__name__=='FitzView':
            view.resized.connect(self.updateZoom)

    def updateZoom(self, view):
        data=self.currentZoom(view)
        mode=data.get('mode', None)
        if mode in ['width', 'height']:
            data['kind']=mode
            self.activate(view=view, **data)

    def currentZoom(self, view):
        return {
             'round': self.zoom_round,
             'factor': self.zoom_factor,
             'mode': view.getAttr('zoom_mode', custom=True)}

    def activate(self, view=None, **kwargs):
        self.updateItemScale(view, **kwargs)
        view.redraw()

    def updateItemScale(self, view, kind, xrange=[1], **kwargs):
        scales={}
        size = view.size()
        weight = size.width()
        height = size.height()
        items=view.getItems()
        for idx, item in items:
            scale=item.getScale()
            dw, dh = item.displayedSize()
            if kind == "width":
                scale = weight / float(dw)
            elif kind == "height":
                scale = height / float(dh)
            elif kind == "adjust":
                scale = min(weight / float(dw), height / float(dh))
            elif kind == "out":
                scale = scale - self.zoom_factor * xrange[0]
            elif kind == "in":
                scale = scale + self.zoom_factor * xrange[0]
            elif type(kind)==float:
                scale=kind
            if scale:
                scale=round(scale, self.zoom_round)
                scales[item]=scale
                view.setAttr('zoom_mode', kind, custom=True)
        for item, scale in scales.items():
            item.setScale(scale)
