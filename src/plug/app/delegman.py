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
            super_view=True
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
                for klass in view.__class__.__mro__:
                    view_name=klass.__name__
                    views=submode.get(view_name, {})
                    if views or not super_view:
                        return views
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
                super_view=super_view)
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
