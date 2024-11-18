import typing as tp

from ..plug import Plug


class Stateman(Plug):
    isMode: bool = True
    default_mode: str = "normal"

    def __init__(self, app: tp.Any) -> None:
        super().__init__(app)

        self.m_keyer = None
        self.m_functor = None
        self.m_passive = False
        self.m_mode: str = "normal"
        self.m_submode: str = None
        self.m_view: tp.Any = None
        self.m_subview: tp.Any = None
        self.m_passive_modes = []

    def setViewDefaultMode(
        self,
        view: tp.Any = None,
    ) -> None:
        mode = None
        if view:
            mode = view.default_mode
        mode = mode or self.default_mode
        self.activate(mode)

    def functor(self):
        return self.m_functor

    def setFunctor(
        self,
        functor: tp.Callable[[...], tp.Any] = None,
    ) -> tp.Callable[[...], tp.Any]:
        self.app.earman.clearKeys(True)
        self.m_functor = functor
        return functor

    def keyer(self):
        return self.m_keyer

    def setKeyer(self, keyer=None):
        self.app.earman.clearKeys(True)
        self.m_keyer = keyer

    def passive(self):
        return self.m_passive

    def setPassive(
        self, modes: tp.List[tp.Any] = None
    ) -> tp.List[tp.Any]:
        cond = False
        if modes:
            cond = True
            if type(modes) == str:
                modes = [modes]
            modes.append("any")
        self.m_passive = cond
        self.m_passive_modes = modes
        self.app.earman.clearKeys(True)
        return modes

    def state(self):
        mode = self.app.stateman.mode() or "any"
        submode = self.app.stateman.submode() or "any"
        view = self.app.stateman.view()
        if view:
            view = view.name
        else:
            view = "any"
        subview = self.app.stateman.subview()
        if subview:
            subview = subview.kind
        else:
            subview = "any"

        state = (mode, submode, view, subview)

        if self.m_passive:
            if not self.m_mode in self.m_passive_modes:
                state = ("any",) * 4
        return state

    def toggle(self, mode: str = None, **kwargs) -> str:
        if mode and self.m_mode != mode:
            return self.activate(mode, **kwargs)
        else:
            return self.octivate(**kwargs)

    def toggleSubmode(self, submode: str=None, **kwargs) -> str:
        if self.m_submode != submode:
            return self.setSubmode(submode, **kwargs)
        else:
            return self.setSubmode(**kwargs)

    def mode(self) -> str:
        return self.m_mode

    def setMode(self, mode: str, **kwargs) -> str:
        mode = mode or self.default_mode
        self.name = mode
        self.m_mode = mode
        return mode

    def submode(self) -> str:
        return self.m_submode

    def setSubmode(
        self, submode: str = None, **kwargs
    ) -> str:
        self.m_submode = submode
        return submode

    def view(self) -> tp.Any:
        return self.m_view

    def setView(
        self,
        view: tp.Any = None,
    ) -> None:
        if not view:
            return
        self.m_view = view
        self.setSubview(view)
        self.setViewDefaultMode(view)

    def subview(self) -> tp.Any:
        return self.m_subview

    def setSubview(
        self,
        view: tp.Any = None,
    ) -> None:
        if not view:
            return
        model = view.model()
        if model and model.isType:
            self.m_subview = view

    def betView(
        self,
        view: tp.Any,
    ) -> None:
        # if self.m_view != view:
        subview=self.subview()
        view = self.app.view.main.current
        print(subview, view)
        if view:
            view.activate()
        elif subview:
            subview.activate()


    def activate(
        self,
        mode: str = None,
        passive: tp.List[str] = [],
        submode: str = None,
        functor: tp.Callable[[...], tp.Any] = None,
        **kwargs,
    ) -> str:
        self.setMode(mode)
        self.setPassive(passive)
        self.setSubmode(submode)
        self.setFunctor(functor)
        return self.m_mode

    def octivate(
        self,
        exit_mode: str = None,
        delisten: bool = False,
        **kwargs,
    ) -> str:
        self.setFunctor()
        self.setPassive()
        self.setSubmode()
        if delisten:
            exit_mode = exit_mode or self.default_mode
        self.setMode(exit_mode)
        return self.m_mode

    def getState(self):
        state = (
            self.mode(),
            self.submode(),
            self.view(),
            self.subview(),
        )
        if self.m_passive:
            if not self.m_mode in self.m_passive_modes:
                state = ("any",) * 4
        return state

    def passiveModes(self):
        return self.m_passive_modes
