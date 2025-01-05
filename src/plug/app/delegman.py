from ..plug import Plug

class Delegman(Plug):

    def setup(self):
        super().setup()
        self.m_functors={}

    def addAgent(
            self, 
            mode=None, 
            submode=None, 
            view=None, 
            action=None,
            functor=None
            ):
        if not mode in self.m_functors:
            self.m_functors[mode]={}
        modes=self.m_functors[mode]
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
            return self.m_functors.get(mode, {})
        elif delegate=='submode':
            mode=self.getAgent(mode=mode, delegate='mode')
            return mode.get(submode, {})
        elif delegate=='view':
            submode=self.getAgent(mode=mode, submode=submode, delegate='submode')
            if type(view)==str:
                return submode.get(view, {})
            else: 
                for klass in view.__class__.__mro__:
                    view_name=klass.__name__
                    views=submode.get(view_name, {})
                    if views or not super_view:
                        return views
                return {}
        elif delegate=='action':
            view=self.getAgent(mode=mode, submode=submode, view=view, delegate='view')
            return view.get(action, {})

    def delegate(
            self, 
            mode=None, 
            submode=None, 
            view=None, 
            action=None, 
            super_view=True,
            delegate='action',
            **kwargs
            ):
        functor=self.getAgent(
                mode=mode, 
                submode=submode, 
                view=view, 
                action=action, 
                delegate=delegate,
                super_view=super_view)
        if functor and delegate=='action':
            return functor(view=view, **kwargs)
        return functor
