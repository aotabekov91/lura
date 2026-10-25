from plug import Plug, deleg

class FitzZoom(Plug):

    zoom_round=3
    zoom_factor = 0.05

    def setup(self):
        super().setup()
        self.app.buffman.viewCreated.connect(
                self.connectView)

    def connectView(self, view):
        if view and view.__class__.__name__=='FitzView':
            view.resized.connect(self.updateZoom)

    @deleg('zoomState@(normal)[FitzView]')
    def zoomState(self, view=None, **kwargs):
        state={}
        if view:
            zoom_kind=view.getAttr(
                    'zoom_kind', custom=True)
            zoom_scale=view.getAttr(
                    'zoom_scale', custom=True)
            if zoom_kind:
                state={
                      'kind': zoom_kind, 
                      'scale': zoom_scale
                      }
        return state 

    @deleg('zoom@(normal)[FitzView]')
    def zoom(self, view=None, kind=None, xrange=[1], scale=None, **kwargs):
        if view:
            size = view.size()
            weight = size.width()
            height = size.height()
            items=view.getItems()
            for idx, item in items:
                item_scale=item.getScale()
                if not scale:
                    dw, dh = item.displayedSize()
                    if kind == "width":
                        item_scale = weight / float(dw)
                    elif kind == "height":
                        item_scale = height / float(dh)
                    elif kind == "adjust":
                        item_scale = min(weight / float(dw), height / float(dh))
                    elif kind == "out":
                        item_scale = item_scale - self.zoom_factor * xrange[0]
                    elif kind == "in":
                        item_scale = item_scale + self.zoom_factor * xrange[0]
                    elif type(kind)==float:
                        item_scale=kind
                    else:
                        return
                else:
                    item_scale=scale
                if item_scale:
                    item_scale=round(item_scale, self.zoom_round)
                    view.setAttr('zoom_kind', kind, custom=True)
                    view.setAttr('zoom_scale', item_scale, custom=True)
                    item.setScale(item_scale)
            view.redraw()
            self.reportStateChange(view)

    def updateZoom(self, view):
        state=self.zoomState(view)
        kind=state.get('kind', None)
        if kind in ['width', 'height']:
            self.zoom(view=view, kind=kind)

    def reportStateChange(self, view):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            data=self.zoomState(view=view)
            normal.stateChanged.emit('zoom', view, data)
