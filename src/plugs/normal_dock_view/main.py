from plug import Plug

class DockViewNormal(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('DockNormal')
        if holder:
            holder.addAgent('goTo', 'DockView', self)
            holder.addAgent('hide', 'DockView', self)
            holder.addAgent('close', 'DockView', self)
            holder.addAgent('create', 'DockView', self)
            holder.addAgent('flipTo', 'DockView', self)
            holder.addAgent('moveTo', 'DockView', self)

    def activate(self, window=None, action=None, **kwargs):
        if window and action:
            manager=window.manager()
            func=getattr(manager, action, None)
            if func:
                func(**kwargs)
