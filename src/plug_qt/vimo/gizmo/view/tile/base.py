from PyQt6 import QtWidgets

import typing as tp

from plug_qt import vimo

from .layout import TileLayout

class TileView(
        vimo.View,
        QtWidgets.QWidget,
        ):

    canCopy=True
    name='TileView'
    suffix_separator: str = "."
    layout_class: tp.Any = TileLayout
    prefix_keys: tp.List[str] = ["<c-w>(normal)"]

    def close(self, **kwargs):
        return self.m_layout.close(**kwargs)

    def goTo(self, **kwargs):
        leaf=self.m_layout.goTo(**kwargs)
        if leaf and leaf.view:
            leaf.view.activate()
        return leaf

    def zoomTo(self, **kwargs):
        return self.m_layout.zoomTo(**kwargs)

    def moveTo(self, **kwargs):
        return self.m_layout.moveTo(**kwargs)

    def flipTo(self, **kwargs):
        self.m_layout.flipTo(**kwargs)

    def splitTo(
        self,
        view=None,
        focus=True,
        kind="vertical",
        **kwargs,
    ):
        copier=self.app.plugman.getPlug('Copy')
        if copier:
            view = view or self.current
            copy=copier.copy(view)
            if copy:
                orientation = kind == "horizontal"
                self.addView(copy, horizontal=orientation)
                if focus:
                    copy.activate()


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

    def setConfig(self):
        if self.app:
            c = self.app.m_config.get("WidgetTileView", {})
            c.update(self.m_config)
            self.m_config = c

    def setParent(self, parent):
        super().setParent(parent)
        if parent and hasattr(parent, "resized"):
            parent.resized.connect(self.update)

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

    def clear(self):
        self.m_layout.clear()

    def addView(self, view=None, **kwargs):
        if view:
            view.setManager(self)
            self.m_layout.addView(view=view, **kwargs)
            return view

    def insertView(self, idx, view, **kwargs):
        view.setManager(self)
        return self.m_layout.insertView(idx, view, **kwargs)

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
