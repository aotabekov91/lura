from ..plug import Plug

class Delegman(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(
            self, 
            mode=None, 
            submode=None, 
            view=None, 
            action=None,
            functor=None
            ):
        if not mode in self.m_agents:
            self.m_agents[mode]={}
        modes=self.m_agents[mode]
        if not submode in modes:
            modes[submode]={}
        submodes=modes[submode]
        if not view in submodes:
            submodes[view]={}
        submodes[view][action]=functor

    def getAgent(
            self, 
            mode=None, 
            submode=None, 
            view=None, 
            action=None, 
            delegate='action', 
            view_approach='super',
            ):
        if delegate=='mode':
            return self.m_agents.get(mode, {})
        elif delegate=='submode':
            mode=self.getAgent(mode=mode, delegate='mode')
            return mode.get(submode, {})
        elif delegate=='view':
            submode=self.getAgent(mode=mode, submode=submode, delegate='submode')
            if view is None or type(view)==str:
                return submode.get(view, {})
            else: 
                if view_approach=='own':
                    view_name=view.__class__.__name__
                    return submode.get(view_name, {})
                elif view_approach=='super':
                    all_views={}
                    for klass in view.__class__.__mro__:
                        view_name=klass.__name__
                        views=submode.get(view_name, {})
                        all_views.update(views)
                    return all_views
                elif view_approach=='manager':
                    raise
        elif delegate=='action':
            view=self.getAgent(mode=mode, submode=submode, view=view, delegate='view')
            return view.get(action, {})
        return {}

    def delegate(
            self, 
            mode=None, 
            submode=None, 
            view=None, 
            action=None, 
            super_view=True,
            delegate='action',
            data={},
            add_fields=['view', 'action'],
            ):
        functor=self.getAgent(
                mode=mode, 
                submode=submode, 
                view=view, 
                action=action, 
                delegate=delegate,
                view_approach=super_view)
        if functor and delegate=='action':
            for field in add_fields:
                if not field in data:
                    if field=='mode':
                        data[field]=mode
                    elif field=='submode':
                        data[field]=submode
                    elif field=='action':
                        data[field]=action
                    elif field=='view':
                        data[field]=view
            return functor(**data)
        return functor
