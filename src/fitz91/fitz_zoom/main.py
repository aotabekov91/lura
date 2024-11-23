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
        zoom_round = data.get('round') 
        zoom_factor = data.get('factor') 
        if kind == "out":
            scale = 1.0 - zoom_factor * xrange[0]
            scale = round(scale, zoom_round)
        elif kind == "in":
            scale = 1.0 + zoom_factor * xrange[0]
            scale = round(scale, zoom_round)
        self.updateItemScale(view, kind, data)
        view.redraw()

    def updateItemScale(self, view, kind, data):
        size = view.size()
        weight = size.width()
        height = size.height()
        items=view.getItems()
        for idx, item in items:
            dw, dh = item.displayedSize()
            if kind == "width":
                scale = weight / float(dw)
            elif kind == "height":
                scale = height / float(dh)
            elif kind == "adjust":
                scale = min(weight / float(dw), height / float(dh))
            else:
                scale = float(kind) * float(item.scale)
            data['kind']=scale
            data['mode']=kind
            item.scale=scale
            item.redraw()
