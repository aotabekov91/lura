from plug import Plug, tag, deleg

class Fullscreen(Plug):
        
    def setup(self):
        super().setup()
        self.m_states={}
        self.m_activated=False

    @deleg('setFullscreenState@(normal)')
    def setViewState(self, view, state={}):
        self.m_states[view]=state

    @deleg('getFullscreenState@(normal)')
    def getViewState(self, view):
        return self.m_states.get(view, {})

    def activate(self, view=None, **kwargs):
        view=view or self.app.stateman.view()
        if view:
            manager=view.manager()
            while manager:
                state=self.app.delegman.delegate(
                        mode='normal',
                        action='viewState',
                        view=manager,
                        data={'view': view, 'manager': manager})
                if state:
                    self.m_activated=True
                    self.setViewState(view, state)
                    self.app.delegman.delegate(
                            mode='normal',
                            view=manager,
                            action='activateFullscreen',
                            data={
                                'view': view, 
                                'state': state,
                                'manager': manager,
                                })
                    break
                elif manager:
                    manager=manager.manager()

    def octivate(self, view=None, **kwargs):
        view=view or self.app.stateman.view()
        state=self.getViewState(view)
        if state and view:
            self.m_activated=False
            self.setViewState(view)
            manager=state['manager']
            self.app.delegman.delegate(
                    mode='normal',
                    view=manager,
                    action='octivateFullscreen',
                    data={
                        'view': view, 
                        'state': state,
                        'manager': manager
                        })

    @tag("f(normal)")
    def toggle(self, *args, **kwargs):
        if self.m_activated:
            self.octivate(*args, **kwargs)
        else:
            self.activate(*args, **kwargs)
