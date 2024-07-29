import typing as tp

from plug_qt import vimo
from plug.utils import tag

from .layout import TileLayout


class TileView(vimo.View):
    name='TileView'
    suffix_separator: str = "."
    layout_class: tp.Any = TileLayout
    prefix_keys: tp.List[str] = ["<c-w>(normal)"]
    canCopy=True

    def copy(self, full=False):
        new_tile=self.__class__(app=self.app)
        if not self.current:
            return new_tile
        if not self.checkProp('canCopy', self.current):
            return new_tile
        current_copy=self.current.copy()
        new_tile.addView(view=current_copy)
        current_copy.activate()
        return new_tile

    def child(self, pos, recursive=True):
        if pos.startswith("x") and self.current:
            i = self.current.posIndex()
            pos = pos.replace("x", str(i), 1)
        elif pos.startswith("-1"):
            i = self.count() - 1
            pos = pos.replace("-1", str(i), 1)
        return super().child(pos, recursive)

    @tag("zk(normal)")
    def viewZoomInUp(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="up", xrange=xrange)

    @tag("zK(normal)")
    def viewZoomOutUp(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="up", inc=False, xrange=xrange
        )

    @tag("zj(normal)")
    def viewZoomInDown(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="down", xrange=xrange)

    @tag("zJ(normal)")
    def viewZoomOutDown(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="down", inc=False, xrange=xrange
        )

    @tag("zl(normal)")
    def viewZoomInRight(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="right", xrange=xrange)

    @tag("zL(normal)")
    def viewZoomOutRight(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="right", inc=False, xrange=xrange
        )

    @tag("zh(normal)")
    def viewZoomInLeft(self, xrange=[1], **kwargs):
        self.m_layout.resize(kind="left", xrange=xrange)

    @tag("zH(normal)")
    def viewZoomOutLeft(self, xrange=[1], **kwargs):
        self.m_layout.resize(
            kind="left", inc=False, xrange=xrange
        )

    @tag("gg(normal)")
    def viewGoToFirst(self, **kwargs):
        self.viewGoTo(kind="first")

    @tag("G(normal)")
    def viewGoToLast(self, xrange=None, **kwargs):
        self.viewGoTo(xrange=xrange, kind="last")

    @tag("v(normal)")
    def splitVertically(self):
        self.split(kind="vertical")

    @tag("s(normal)")
    def splitHorizontally(self):
        self.split(kind="horizontal")

    @tag("k(normal)")
    def viewGoToUp(self):
        self.viewGoTo(kind="up")

    @tag("j(normal)")
    def viewGoToDown(self):
        self.viewGoTo(kind="down")

    @tag("l(normal)")
    def viewGoToRight(self):
        self.viewGoTo(kind="right")

    @tag("h(normal)")
    def viewGoToLeft(self):
        self.viewGoTo(kind="left")

    @tag("n(normal)")
    def viewGoToNext(self):
        self.viewGoTo(kind="next")

    @tag("p(normal)")
    def goToPrevView(self):
        self.viewGoTo(kind="prev")

    @tag("x(normal)")
    def viewFlip(self):
        n, c = self.m_layout.swap()
        if n and n.view:
            n.view.activate()

    @tag("e(normal)")
    def equalizeRatio(self):
        self.m_layout.equalize()

    @tag("f(normal)")
    def toggleSplit(self):
        self.m_layout.toggleSplit()

    @tag("~gw(normal)")
    def viewGoTo(self, kind=None, xrange=None):
        n = self.m_layout.goTo(kind, xrange)
        if n and n.view:
            n.view.activate()
        return n

    @tag("~gW(normal)")
    def viewMoveTo(self, xrange=None, **kwargs):
        return self.m_layout.move(xrange=xrange, **kwargs)

    @tag("K(normal)")
    def viewMoveToUp(self, xrange=[1]):
        self.viewMoveTo(kind="up", xrange=xrange)

    @tag("J(normal)")
    def viewMoveToDown(self, xrange=[1]):
        self.viewMoveTo(kind="down", xrange=xrange)

    @tag("H(normal)")
    def viewMoveToLeft(self, xrange=[1]):
        self.viewMoveTo(kind="left", xrange=xrange)

    @tag("L(normal)")
    def viewMoveToRight(self, xrange=[1]):
        self.viewMoveTo(kind="right", xrange=xrange)

    def setConfig(self):
        if self.app:
            c = self.app.m_config.get("WidgetTileView", {})
            c.update(self.m_config)
            self.m_config = c

    def setParent(self, p):
        super().setParent(p)
        if p and hasattr(p, "resized"):
            p.resized.connect(self.update)

    def setup(self):
        self.setConfig()
        super().setup()
        self.setContentsMargins(0, 0, 0, 0)
        self.m_layout = self.layout_class(self)
        self.m_layout.geometryChanged.connect(
            self.geometryChanged
        )

    def focus(self, increment=1):
        if self.m_layout.count() < 2:
            v = self.currentView()
            if v:
                v.setFocus()
        else:
            cv = self.currentView()
            idx = self.indexOf(cv)
            idx += increment
            if idx >= self.m_layout.count():
                idx = 0
            elif idx < 0:
                idx = self.m_layout.count() - 1
            v = self.widget(idx)
            if v:
                v.activate()

    @tag("c(normal)")
    def closeView(self, v=None, **kwargs):
        l = self.m_layout
        p = l.findSibling(kind="prev")
        n = l.findSibling(kind="next")
        v = v or self.current
        l.removeView(v)
        if p and v != p:
            p.activate()
        elif n:
            n.activate()

    def clear(self):
        self.m_layout.clear()

    def toggleFullscreen(self, v):
        self.m_layout.toggleFullscreen(v)

    def addView(self, view, **kwargs):
        view.setManager(self)
        self.m_layout.addView(view, **kwargs)
        return view

    def insertView(self, idx, v, **kwargs):
        v.setManager(self)
        return self.m_layout.insertView(idx, v, **kwargs)

    def setView(self, *args, **kwargs):
        self.m_layout.setView(*args, **kwargs)

    def removeView(self, view=None, **kwargs):
        l = self.m_layout
        if not view:
            c = self.m_layout.current_leaf
            if not c:
                return
            view = c.view
        return l.removeView(view)

    def split(
        self,
        view=None,
        focus=True,
        kind="vertical",
    ):
        view = view or self.current
        if not view:
            raise
        copier=self.app.plugman.plugs.get('Copy')
        if not copier:
            return
        view_copy=copier.copy(view)
        if not view_copy:
            return
        stand = kind == "horizontal"
        self.addView(view_copy, horizontal=stand)
        if focus:
            view_copy.activate()

    def update(self):
        self.m_layout.update()

    def count(self):
        return self.m_layout.count()

    @property
    def current(self):
        return self.m_layout.current

    @property
    def previous(self):
        return self.m_layout.previous

    def activate(self, descend=True, **kwargs):
        super().activate(**kwargs)
        if self.current and descend:
            self.current.activate()
