from plug import Plug, deleg

class BrowserZoom(Plug):

    zoom_factor=0.05

    @deleg('zoom@(normal)[BrowserView]')
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

    @deleg('zoomState@(normal)[BrowserView]')
    def zoomState(self, view=None, **kwargs):
        if view:
            page=view.page()
            return {'scale': page.zoomFactor()}

    def reportStateChange(self, view):
        data=self.zoomState(view)
        normal=self.app.plugman.getPlug('Normal')
        if data and normal:
            normal.stateChanged.emit('zoom', view, data)
