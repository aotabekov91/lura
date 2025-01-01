from plug import Plug

class BrowserZoom(Plug):

    zoom_factor=0.05

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def zoomState(self, view=None, **kwargs):
        if view:
            page=view.page()
            return {'scale': page.zoomFactor()}

    def addAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            normal.addAgent('zoom', 'BrowserView', self)
            normal.addAgent('zoomState', 'BrowserView', self)

    def activate(self, action=None, view=None, **kwargs):
        func = getattr(self, action, None)
        if view and func:
            return func(view=view, **kwargs)

    def zoom(self, view=None, kind=None, scale=None, xrange=[1], **kwargs):
        if view:
            page=view.page()
            data=self.zoomState(view)
            if not scale and data:
                current_scale=data['scale']
                if kind=='in':
                    scale=current_scale+self.zoom_factor*xrange[-1]
                elif kind=='out':
                    scale=current_scale-self.zoom_factor*xrange[-1]
            if scale:
                page.setZoomFactor(scale)
                self.reportStateChange(view)

    def reportStateChange(self, view):
        data=self.zoomState(view)
        normal=self.app.plugman.getPlug('Normal')
        if data and normal:
            normal.stateChanged.emit('zoom', view, data)
