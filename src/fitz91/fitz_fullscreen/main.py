from plug import Plug

class FitzFullscreen(Plug):

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
            holder.addAgent('FitzView', self)

    def saveState(self, view, state={}):
        self.m_states[view]=state

    def getState(self, view):
        return self.m_states.get(view, {})

    def activate(self, view=None, **kwargs):
        if view:
            size = view.size()
            idx = view.posIndex()
            manager = view.manager()
            geometry = view.geometry()
            updateView = lambda: self.updateView(view)
            state={'idx':idx, 
                  'size': size,
                  'manager': manager,
                  'geometry': geometry,
                  'updater': updateView,
                  }
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

    def octivate(self, view):
        state=self.getState(view)
        idx=state.get('idx', None)
        size=state.get('size', None)
        updateView=state.get('updater', None)
        geometry=state.get('geometry', None)
        overlay=self.app.plugman.getPlug('Overlay')
        parent = overlay.getOverlay(self.app.view)
        if parent:
            parent.resized.disconnect(updateView)
        manager = view.manager()
        manager.octivate()
        manager.removeView(view)
        manager=state.get('manager', None)
        view.setManager(manager)
        manager.insertView(
            view=view,
            idx=idx,
            size=size,
            geometry=geometry)
        self.saveState(view)
        view.activate()

    def updateView(self, view):
        manager=view.manager()
        view.setGeometry(manager.geometry())
