import typing as tp

from ..plug import Plug

class Stateman(Plug):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.m_mode = None 
        self.m_keyer = None
        self.m_functor = None
        self.m_passive = False
        self.m_submode = None
        self.m_view = None
        self.m_subview = None
        self.m_passive_modes = []

    def functor(self):
        return self.m_functor

    def setFunctor(self, *args, functor=None, **kwargs):
        self.app.earman.clearKeys(True)
        self.m_functor = functor
        return functor

    def keyer(self):
        return self.m_keyer

    def setKeyer(self, *args, keyer=None, **kwargs):
        self.app.earman.clearKeys(True)
        self.m_keyer = keyer

    def passive(self):
        return self.m_passive

    def setPassive(self, *args, passive = [], **kwargs) -> tp.List[tp.Any]:
        cond = False
        if passive:
            cond = True
            if type(passive) == str:
                passive = [passive]
            passive.append("any")
        self.m_passive = cond
        self.m_passive_modes = passive
        self.app.earman.clearKeys(True)
        return passive

    def state(self):
        if self.m_passive:
            if not self.m_mode in self.m_passive_modes:
                return ("any",) * 4
        view = self.view() or 'any'
        mode = self.mode() or "any"
        submode = self.submode() or "any"
        subview = self.app.stateman.subview() or 'any'
        if view:
            view = view.name
        if subview:
            subview = subview.kind
        return  (mode, submode, view, subview)

    def mode(self):
        return self.m_mode

    def setMode(self, *args, mode='normal', toggle_mode=False, **kwargs) -> str:
        if toggle_mode and mode==self.m_mode:
            self.m_mode='normal'
        else:
            self.m_mode = mode
        return self.m_mode

    def submode(self) -> str:
        return self.m_submode

    def setSubmode(self, *args, submode=None, toggle_submode=False, **kwargs):
        if toggle_submode and submode==self.m_submode:
            self.m_submode=None
        else:
            self.m_submode = submode
        return self.m_submode

    def view(self) -> tp.Any:
        return self.m_view

    def setView(self, view=None, **kwargs) -> None:
        if view:
            self.m_view = view
            self.setMode(**kwargs)
            self.setSubview(view=view)

    def subview(self) -> tp.Any:
        return self.m_subview

    def setSubview(self, view = None, **kwargs) -> None:
        if view and view.isSubview:
            self.m_subview = view

    def betView(self, *args, **kwargs) -> None:
        view = self.app.view.main.current
        if view and view!=self.m_view:
            view.activate()
        elif self.m_subview and self.m_view!=self.m_subview:
            self.m_subview.activate()

    def activate(self, *args, **kwargs):
        self.setMode(*args, **kwargs)
        self.setPassive(*args, **kwargs)
        self.setSubmode(*args, **kwargs)
        self.setFunctor(*args, **kwargs)
        return self.m_mode

    def passiveModes(self):
        return self.m_passive_modes
