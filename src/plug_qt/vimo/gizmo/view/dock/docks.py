from PyQt6 import QtCore, QtWidgets

from plug_qt.vimo import View

from .dock import DockView


class Docks(
    View,
    QtCore.QObject,
):

    number_mapping={1:'L', 2:'U', 3:'R', 4:'D'}

    def setup(self):
        super().setup()
        self.m_docks = []
        self.m_current = None
        self.createDocks()

    def createDocks(self):
        parent=self.parent()
        parent.setCorner(
            QtCore.Qt.Corner.TopLeftCorner,
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        parent.setCorner(
            QtCore.Qt.Corner.TopRightCorner,
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
        )
        parent.setCorner(
            QtCore.Qt.Corner.BottomLeftCorner,
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        parent.setCorner(
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
            loc = loc[0].upper()
            dock = DockView(
                loc=loc,
                label=loc,
                pindex=i + 1,
                app=self.app,
                manager=self,
                identifier=loc,
            )
            dock.setContentsMargins(0, 0, 0, 0)
            dock.title = QtWidgets.QWidget()
            dock.setTitleBarWidget(dock.title)
            parent.addDockWidget(r, dock)
            setattr(self, f"{loc}", dock)
            self.m_docks += [dock]
        self.hide(kind='all')

    def moveTo(self, kind, dock=None, **kwargs):
        dock = dock or self.m_current
        area = getattr(self, kind, None)
        if area and dock and dock.isVisible():
            area = self.addView(dock.current, kind)
            if area:
                area.activate(area.current)

    def goTo(self, kind=None, **kwargs):
        dock = getattr(self, kind, None)
        if dock and dock.isVisible():
            dock.current.activate(**kwargs)

    def zoomTo(self, dock=None, **kwargs):
        dock = dock or self.m_current
        if dock and dock.isVisible():
            dock.scale(**kwargs)

    def hide(self, xrange=[], kind=None, **kwargs):
        if kind=='all':
            for dock in self.m_docks: 
                dock.hide()
        elif xrange:
            idx=xrange[-1]
            loc=self.number_mapping.get(idx, None)
            dock = getattr(self, loc, None)
            if dock:
                dock.hide()
                dock.octivate(**kwargs)

    def addView(self, view=None, loc=None, **kwargs):
        if loc and view:
            dock = getattr(self, loc, None)
            if dock:
                self.removeView(view)
                dock.addView(view)
            return dock

    def removeView(self, view=None, **kwargs):
        dock = getattr(view, "dock", None)
        if dock:
            dock.removeView(view)
        return view

    def setCurrent(self, dock):
        self.m_current = dock
