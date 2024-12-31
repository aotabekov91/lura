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

    def addAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            normal.addAgent('zoom', 'BrowserView', self)

    def currentZoom(self, view):
        page=view.page()
        return page.zoomFactor()

    def activate(
            self, 
            view=None, 
            kind=None, 
            xrange=[1], 
            **kwargs):
        if view:
            page=view.page()
            factor=self.currentZoom(view)
            if kind=='in':
                factor=factor+self.zoom_factor*xrange[-1]
            elif kind=='out':
                factor=factor-self.zoom_factor*xrange[-1]
            page.setZoomFactor(factor)
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            data=self.currentZoom(view)
            normal.stateChanged('zoom', view, data)
