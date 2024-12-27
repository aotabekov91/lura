from plug import Plug

class BrowserZoom(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Zoom')
        if holder:
            holder.addAgent('BrowserView', self)

    def activate(
            self, 
            view=None, 
            kind=None, 
            data={}, 
            xrange=[1], 
            **kwargs):
        if view:
            page=view.page()
            value=data.get('factor', 0.05)
            factor=self.currentZoom(view)
            if kind=='in':
                factor=factor+value*xrange[-1]
            elif kind=='out':
                factor=factor-value*xrange[-1]
            page.setZoomFactor(factor)

    def currentZoom(self, view):
        page=view.page()
        return page.zoomFactor()
