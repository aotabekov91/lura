from plug import Plug

class BrowserNormal(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Normal')
        if holder:
            holder.addAgent('goTo', 'BrowserView', self)

    def currentPosition(self, view=None, kind='percentage'):
        # todo: return percentage/pixel position
        if kind=='percentage':
            return 0
        elif kind=='pixel':
            raise

    def activate(
            self, 
            view=None, 
            kind=None, 
            xrange=[1], 
            xdelta=100, 
            ydelta=100, 
            **kwargs):
        if view:
            code=None
            page=view.page()
            size=page.contentsSize()
            if kind=='up':
                ydelta*=-1*xrange[-1]
                code=view.assemble('window', 'scrollBy', 0, ydelta)
            elif kind=='down':
                ydelta*=xrange[-1]
                code=view.assemble('window', 'scrollBy', 0, ydelta)
            elif kind=='left':
                xdelta*=-1*xrange[-1]
                code=view.assemble('window', 'scrollBy', xdelta, 0)
            elif kind=='right':
                xdelta*=xrange[-1]
                code=view.assemble('window', 'scrollBy', xdelta, 0)
            elif kind=='first':
                ydelta=-1*size.height()
                code=view.assemble('window', 'scrollBy', 0, ydelta)
            elif kind=='last':
                ydelta=size.height()
                code=view.assemble('window', 'scrollBy', 0, ydelta)
            if code:
                page.runJavaScript(code)
