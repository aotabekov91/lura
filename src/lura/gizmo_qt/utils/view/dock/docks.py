from PyQt6 import QtCore, QtWidgets

from lura.qt.vimo import View
from lura.gizmo.utils import tag

from .dock import DockView


class Docks(
    View,
    QtCore.QObject,
):
    prefix_keys = ["<c-d>(normal)"]

    def __init__(
            self, 
            app=None, 
            parent=None, 
            **kwargs):
        super().__init__(
            app=app,
            parent=parent,
            **kwargs,
        )

        self.m_docks = []
        self.m_current = None
        self.m_parent = parent
        self.createDocks()

    def createDocks(self):
        self.m_parent.setCorner(
            QtCore.Qt.Corner.TopLeftCorner,
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        self.m_parent.setCorner(
            QtCore.Qt.Corner.TopRightCorner,
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
        )
        self.m_parent.setCorner(
            QtCore.Qt.Corner.BottomLeftCorner,
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        self.m_parent.setCorner(
            QtCore.Qt.Corner.BottomRightCorner,
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
        )
        locs = {
            "left": QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
            "up": QtCore.Qt.DockWidgetArea.TopDockWidgetArea,
            "right": QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            "down": QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,
        }
        for i, (loc, r) in enumerate(locs.items()):
            l = loc[0].upper()
            d = DockView(
                loc=loc,
                label=l,
                pindex=i + 1,
                app=self.app,
                manager=self,
                identifier=l,
            )
            d.setContentsMargins(0, 0, 0, 0)
            d.title = QtWidgets.QWidget()
            d.setTitleBarWidget(d.title)
            self.m_parent.addDockWidget(r, d)
            setattr(self, f"{loc}", d)
            self.m_docks += [d]
        self.hideAll()

    def addView(self, w, loc):
        d = getattr(self, loc, None)
        if d:
            self.removeView(w)
            d.addView(w)
        return d

    def removeView(self, w):
        d = getattr(w, "dock", None)
        if d:
            d.removeView(w)
        return w

    @tag("Hnormal")
    def hideAll(self):
        [d.hide() for d in self.m_docks]

    def move(
        self,
        kind,
        dock=None,
        **kwargs,
    ):
        d = dock or self.m_current
        n = getattr(self, kind, None)
        if n and d and d.isVisible():
            n = self.addView(d.current, kind)
            if n:
                n.activate(n.current)

    def goTo(self, kind=None, **kwargs):
        d = getattr(self, kind, None)
        if d and d.isVisible():
            d.current.setFocus()

    def scale(self, kind, xrange=[1], dock=None, **kwargs):
        d = dock or self.m_current
        if d and d.isVisible():
            d.scale(kind, xrange)

    # def toggleFullscreen(self, dock=None, **kwargs):
    #     d = dock or self.m_current
    #     if d and d.isVisible():
    #         d.toggleFullscreen()

    def setCurrent(self, dock):
        self.m_current = dock
        # for d in self.m_docks:
        #     if d == dock:
        #         continue
        #     if d.fullscreen and d.isVisible():
        #         d.toggleFullscreen()
