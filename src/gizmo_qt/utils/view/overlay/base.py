from PyQt6 import QtCore, QtGui, QtWidgets

from gizmo_qt import vimo

from .clock import Clock
from .input import OverlayInput
from .list import OverlayList
from .view import OverlayGraphicsView


class OverlayView(vimo.View, QtWidgets.QWidget):
    def __init__(
        self,
        *args,
        objectName="Overlay",
        **kwargs,
    ):
        self.views = {}
        self.dark = True
        self.blur = False
        self.current = None
        self.previous = None
        self.activated = True
        super().__init__(
            *args, objectname=objectName, **kwargs
        )
        self.setPalette(
            QtGui.QPalette(
                QtCore.Qt.GlobalColor.transparent
            )
        )
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.resized.connect(self.updateOverlayPosition)
        self.setupParts()
        self.setupUI()
        self.hide()

    def setupUI(self):
        self.m_blur = self.blur
        self.m_dark = self.dark
        c = self.app.m_config.get(self.name, {})
        self.m_config.update(c)
        blur_color = self.m_config.get(
            "blur_color", (25, 25, 25, 200)
        )
        dark_color = self.m_config.get(
            "dark_color", "black"
        )
        self.blur_color = QtGui.QColor(*blur_color)
        self.dark_color = QtGui.QColor(dark_color)

    def setupParts(self):
        self.list = OverlayList(
            parent=self,
            app=self.app,
            manager=self,
            objectName="OverlayList",
        )
        self.clock = Clock(
            parent=self,
            app=self.app,
            manager=self,
            objectName="OverlayClock",
        )
        self.input = OverlayInput(
            parent=self,
            app=self.app,
            manager=self,
            objectName="OverlayInput",
        )
        self.view = OverlayGraphicsView(
            parent=self,
            app=self.app,
            manager=self,
            objectName="OverlayGraphicsView",
        )

    def paintEvent(self, event):
        if self.m_blur or self.m_dark:
            qp = QtGui.QPainter()
            qp.begin(self)
            if self.m_blur:
                qp.setBrush(self.blur_color)
            else:
                qp.setBrush(self.dark_color)
            qp.drawRect(self.rect())
            qp.end()
        else:
            super().paintEvent(event)

    def addView(self, v, **kwargs):
        v.setParent(self)
        v.setManager(self)
        self.views[id(v)] = v

    def removeView(self, v, **kwargs):
        self.hide()
        v.setManager()
        v.setParent(None)
        self.m_blur = self.blur
        self.views.pop(id(v))

    def insertView(self, idx, v, **kwargs):
        pass

    def betView(self, v, **kwargs):
        v.hide()
        self.m_blur = False
        self.m_dark = False
        self.app.ui.update()
        rec = kwargs.get("recursive")
        if rec:
            self.octivate()

    def setView(
        self,
        *args,
        view=None,
        blur=False,
        dark=True,
        active_views=[],
        **kwargs,
    ):
        for i in self.views.values():
            if i in active_views:
                continue
            if i == view:
                continue
            i.hide()
        self.m_blur = blur
        self.m_dark = dark
        c, p = view, self.current
        self.current, self.previous = c, p
        self.show()
        view.show(**kwargs)
        view.setFocus()
        self.updateViewPosition(view)
        self.app.ui.update()

    def updateViewPosition(self, v=None):
        if not v:
            return
        uf = getattr(v, "updatePosition", None)
        if uf:
            uf()

    def updateOverlayPosition(self):
        self.resized.disconnect(self.updateOverlayPosition)
        g = self.geometry()
        if self.checkProp("bar", self.app.ui):
            bsize = self.app.ui.bar.size()
            bheight = bsize.height()
            h = g.height() - bheight
            g.setHeight(h)
        self.setGeometry(g)
        self.resized.connect(self.updateOverlayPosition)
