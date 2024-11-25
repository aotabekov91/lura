from plug import Plug

class TabViewNormal(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('TabNormal')
        if holder:
            holder.addAgent('goTo', 'TabView', self)
            holder.addAgent('close', 'TabView', self)
            holder.addAgent('create', 'TabView', self)
            holder.addAgent('flipTo', 'TabView', self)
            holder.addAgent('moveTo', 'TabView', self)

    def activate(self, window=None, action=None, **kwargs):
        if window and action:
            func=getattr(window, action, None)
            if func:
                func(**kwargs)
