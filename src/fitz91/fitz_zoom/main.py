from plug import Plug

class FitzZoom(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        zoomer=self.app.plugman.getPlug('Zoom')
        if zoomer:
            zoomer.addAgent('FitzView', self)

    def activate(self, view=None, kind=None, xrange=[1], data={}, **kwargs):
        self.updateItemScale(view, kind, data, xrange)
        view.redraw()

    def updateItemScale(self, view, kind, data, xrange):
        zoom_factor = data.get('factor') 
        zoom_round = data.get('round', 3) 
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
                scale = scale - zoom_factor * xrange[0]
            elif kind == "in":
                scale = scale + zoom_factor * xrange[0]
            elif type(kind)==float:
                scale=kind
            if scale:
                data['kind']=scale
                data['mode']=kind
                item.setScale(round(scale, zoom_round))
