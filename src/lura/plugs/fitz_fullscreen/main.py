from plug import Plug, deleg

class FitzFullscreen(Plug):

    def setup(self):
        super().setup()
        self.m_states={}
        self.setupOverlayView()

    def setupOverlayView(self):
        overlay_plug=self.app.plugman.getPlug('Overlay')
        self.m_overlay=overlay_plug.getOverlay(
                view=self.app.view)

    def setState(self, view, state={}):
        self.m_states[view]=state

    def getState(self, view):
        return self.m_states.get(view, {})

    @deleg('toggleFullscreen@(normal)[TileView]')
    def toggle(self, view=None, **kwargs):
        state=self.getState(view)
        if state:
            self.octivate(view=view, **kwargs)
        else:
            self.activate(view=view, **kwargs)

    def activate(self, view=None, **kwargs):
        if view:
            manager = view.manager()
            updateView = lambda: self.updateView(view)
            leaf=manager.getLeaf(view)
            parent_leaf=leaf.parentLeaf()
            state={
                    'size': view.size(),
                    'manager': manager, 
                    'idx': view.posIndex(),
                    'geometry': view.geometry(), 
                    'updater': updateView,
                    'horizontal': parent_leaf.horizontal, 
                  }
            self.setState(view, state)
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
        if state:
            idx=state.get('idx', None)
            size=state.get('size', None)
            updateView=state.get('updater', None)
            geometry=state.get('geometry', None)
            horizontal=state.get('horizontal', None)
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
                horizontal=horizontal,
                geometry=geometry)
            self.setState(view)
            view.activate()

    def updateView(self, view):
        manager=view.manager()
        view.setGeometry(manager.geometry())
