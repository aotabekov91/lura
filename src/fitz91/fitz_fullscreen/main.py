from plug import Plug

class FitzFullscreen(Plug):

    def setup(self):
        super().setup()
        self.m_states={}
        if self.app.running:
            self.addToFullscreener()
        else:
            self.app.appSoonStarts.connect(
                    self.addToFullscreener)

    def addToFullscreener(self):
        fullscreener=self.app.plugman.plugs.get(
                'Fullscreen')
        if fullscreener:
            fullscreener.addFullscreener(
                    'FitzView', self)

    def saveState(self, view, state={}):
        self.m_states[view]=state

    def state(self, view):
        return self.m_states.get(view, {})

    def activate(self, view):
        size = view.size()
        idx = view.posIndex()
        manager = view.manager()
        geometry = view.geometry()
        updater = lambda: self.update(view)
        state={'idx':idx, 
              'size': size,
              'manager': manager,
              'updater': updater,
              'geometry': geometry,
              }
        self.saveState(view, state)
        manager.removeView(view)
        overlay = self.app.view.overlay
        overlay.addView(view)
        overlay.setView(view)
        overlay.resized.connect(updater)
        view.activate(recursive=True)
        updater()

    def octivate(self, view):
        manager = view.manager()
        manager.removeView(view)
        manager.octivate()
        state=self.state(view)
        idx=state.get('idx', None)
        size=state.get('size', None)
        manager=state.get('manager', None)
        updater=state.get('updater', None)
        geometry=state.get('geometry', None)
        overlay = self.app.view.overlay
        overlay.resized.disconnect(updater)
        view.setManager(manager)
        manager.insertView(
            view=view,
            idx=idx,
            size=size,
            geometry=geometry)
        self.saveState(view)
        view.activate()

    def update(self, view):
        overlay = self.app.view.overlay
        view.setGeometry(overlay.geometry())
