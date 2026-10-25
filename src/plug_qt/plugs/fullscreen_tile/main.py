from plug import Plug, deleg

class TileViewFullscreen(Plug):

    def updateView(self, view):
        manager=view.manager()
        view.setGeometry(manager.geometry())

    @deleg('viewState@(normal)[TileView]')
    def tilePaneState(self, view=None, manager=None, **kwargs):
        if view and manager:
            leaf=manager.getLeaf(view)
            if leaf:
                parent_leaf=leaf.parentLeaf()
                horizontal=parent_leaf.horizontal
            else:
                horizontal=True
            return {
                    'manager': manager, 
                    'size': view.size(),
                    'idx': view.posIndex(),
                    'horizontal': horizontal,
                    'geometry': view.geometry(), 
                    'view_updater': lambda: self.updateView(view),
                    }
        return {}

    @deleg('activateFullscreen@(normal)[TileView]')
    def activate(self, view=None, manager=None, state={}, **kwargs):
        if view and manager:
            view_updater=state['view_updater']
            overlay_view = self.app.delegman.delegate(
                    mode='normal',
                    action='getOverlay',
                    data={'view': self.app.view})
            if overlay_view:
                manager.removeView(view)
                overlay_view.addView(view)
                overlay_view.setView(view)
                overlay_view.resized.connect(view_updater)
                view.activate(recursive=True)
                view_updater()

    @deleg('octivateFullscreen@(normal)[TileView]')
    def octivate(self, view=None, manager=None, state={}, **kwargs):
        if state and view and manager:
            idx=state.get('idx')
            size=state.get('size')
            geometry=state.get('geometry')
            horizontal=state.get('horizontal')
            view_updater=state.get('view_updater')
            overlay_view=self.app.delegman.delegate(
                    mode='normal',
                    action='getOverlay',
                    data={'view': self.app.view})
            overlay_manager = view.manager()
            overlay_manager.octivate()
            overlay_manager.removeView(view)
            # todo: view_updater is not connected raises issue
            # overlay_view.resized.disconnect(view_updater)
            view.setManager(manager)
            # todo: inserts to the first position regardless of idx
            manager.insertView(
                view=view,
                idx=idx,
                size=size,
                horizontal=horizontal,
                geometry=geometry)
            view.activate()
