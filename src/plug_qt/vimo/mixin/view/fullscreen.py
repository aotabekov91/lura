from PyQt6 import QtCore

from plug.utils import tag


class Fullscreen:
    isFullscreen = False
    canFullscreen = True
    fullscreenToggled = QtCore.pyqtSignal(object)

    @tag("f(normal)[^]")
    def toggleFullscreen(self, *args, **kwargs):
        m = self.manager()
        f = self.toggleViewFullscreen
        if m:
            f = getattr(m, "toggleFullscreen", f)
        f(self, **kwargs)
        self.fullscreenToggled.emit(self.isFullscreen)

    def toggleViewFullscreen(
        self,
        *args,
        view=None,
        kind=None,
        **kwargs,
    ):
        v = view or self
        if getattr(v, "isFullscreen", False):
            m = v.manager()
            m.removeView(v)
            m.octivate()
            m = getattr(v, "m_prev_man", None)
            if m and m != self:
                f = getattr(m, "toggleFullscreen", None)
                if f:
                    return f(v)
            v.isFullscreen = False
            nm = o = v.app.ui.overlay
            if kind:
                nm = getattr(nm, kind, nm)
            o.resized.disconnect(v.m_update_func)
            v.setManager(v.m_prev_man)
            v.m_prev_man.insertView(
                view=v,
                idx=v.m_prev_pos,
                size=v.m_prev_size,
                geometry=v.m_prev_geom,
            )
            v.m_prev_pos = None
            v.m_prev_man = None
            v.m_prev_geom = None
            v.m_prev_size = None
            v.m_update_func = None
            v.isFullscreen = False
            v.activate()
        else:
            s = v.size()
            m = v.manager()
            g = v.geometry()
            i = v.posIndex()
            m.removeView(v)
            v.m_prev_pos = i
            v.m_prev_man = m
            v.m_prev_geom = g
            v.m_prev_size = s
            nm = o = v.app.ui.overlay
            if kind:
                nm = getattr(nm, kind, nm)
            nm.addView(v)
            nm.setView(v)
            v.isFullscreen = True
            uf = lambda: self.updateFullscreenPosition(
                view, kind
            )
            o.resized.connect(uf)
            v.m_update_func = uf
            v.activate(recursive=True)
            uf()

    def updateFullscreenPosition(
        self, view=None, kind=None
    ):
        view = view or self
        nm = o = self.app.ui.overlay
        if kind:
            nm = getattr(o, kind, o)
        view.setGeometry(nm.geometry())
