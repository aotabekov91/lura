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

    def moveTo(self, kind=None, dock=None, view=None, **kwargs):
        dock = getattr(self, kind, None)
        if not view and self.m_current:
            view=self.m_current.current
        if view:
            self.addView(view=view, dock=dock, **kwargs)
            view.activate(**kwargs)

    def goTo(self, kind=None, **kwargs):
        dock = getattr(self, kind, None)
        # if dock and dock.isVisible():
        if dock and dock.current:
            dock.current.activate(**kwargs)

    def zoomTo(self, dock=None, **kwargs):
        dock = dock or self.m_current
        # if dock and dock.isVisible():
        if dock:
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

    def addView(self, view=None, loc=None, dock=None, **kwargs):
        if not dock and loc:
            dock = getattr(self, loc, None)
        if dock and view:
            self.removeView(view=view)
            dock.addView(view=view)
            return dock

    def removeView(self, view=None, **kwargs):
        if view:
            manager=view.manager()
            if manager:
                manager.hide()
                manager.removeView(view)
                manager.octivate(**kwargs)
            return view

    def setCurrent(self, dock):
        self.m_current = dock
