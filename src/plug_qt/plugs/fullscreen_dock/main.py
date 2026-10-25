from plug import Plug, deleg

class DockViewFullscreen(Plug):

    def updateView(self, view):
        manager=view.manager()
        view.setGeometry(manager.geometry())

    @deleg('viewState@(normal)[DockView]')
    def dockViewState(self, view=None, manager=None, **kwargs):
        if view and manager:
            return {
                    'manager': manager, 
                    'size': view.size(),
                    'idx': view.posIndex(),
                    'geometry': view.geometry(), 
                    'view_updater': lambda: self.updateView(view),
                    }
        return {}

    @deleg('activateFullscreen@(normal)[DockView]')
    def activate(self, view=None, manager=None, state={}, **kwargs):
        if view and manager and state:
            view_updater=state['view_updater']
            overlay_plug=self.app.plugman.getPlug('Overlay')
            overlay_view = overlay_plug.getOverlay(self.app.view)
            if overlay_view:
                manager.removeView(view)
                overlay_view.addView(view)
                overlay_view.setView(view)
                # overlay_view.resized.connect(view_updater)
                view.activate(recursive=True)
                view_updater()

    @deleg('octivateFullscreen@(normal)[DockView]')
    def octivate(self, view=None, state={}, manager=None, **kwargs):
        if state and view and manager:
            overlay_manager=view.manager()
            overlay_manager.betView(view=view)
            # view_updater=state.get('view_updater')
            # overlay_manager.resized.connect(view_updater)
            manager.addView(view=view)
            view.activate(recursive=True)
