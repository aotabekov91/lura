from plug import Plug

class DockFullscren(Plug):

    def setup(self):
        super().setup()
        self.m_states={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        overlay=self.app.plugman.getPlug('Overlay')
        holder=self.app.plugman.getPlug('Fullscreen')
        if holder and overlay:
            holder.addAgent('DockView', self)
            holder.addAgent('OverlayView', self)

    def saveState(self, view, state={}):
        self.m_states[view]=state

    def getState(self, view):
        return self.m_states.get(view, {})

    def activate(self, view=None, **kwargs):
        if view:
            manager = view.manager()
            updateView = lambda: self.updateView(view)
            state={'manager': manager, 'updater': updateView}
            self.saveState(view, state)
            overlay=self.app.plugman.getPlug('Overlay')
            parent = overlay.getOverlay(self.app.view)
            if parent:
                manager.removeView(view)
                parent.addView(view)
                parent.setView(view)
                parent.resized.connect(updateView)
                view.activate(recursive=True)
                updateView()

    def octivate(self, view=None, **kwargs):
        state=self.getState(view)
        if view and state:
            updateView=state.get('updater', None)
            overlay=self.app.plugman.getPlug('Overlay')
            parent = overlay.getOverlay(self.app.view)
            if parent:
                parent.resized.disconnect(updateView)
            view.octivate(recursive=True)
            manager = view.manager()
            manager.removeView(view)
            manager=state.get('manager', None)
            view.setManager(manager)
            manager.addView(view=view)
            self.saveState(view)
            view.activate(recursive=True)

    def updateView(self, view):
        manager=view.manager()
        view.setGeometry(manager.geometry())
