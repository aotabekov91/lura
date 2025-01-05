from plug import Plug

class TileWindowNormal(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('WindowNormal')
        if holder:
            holder.addAgent('goTo', 'TileView', self)
            holder.addAgent('close', 'TileView', self)
            holder.addAgent('flipTo', 'TileView', self)
            holder.addAgent('zoomTo', 'TileView', self)
            holder.addAgent('moveTo', 'TileView', self)
            holder.addAgent('splitTo', 'TileView', self)

    def delegate(self, window=None, action=None, **kwargs):
        if window and action:
            func=getattr(window, action, None)
            if func:
                func(**kwargs)
