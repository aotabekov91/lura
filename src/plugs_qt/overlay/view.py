from PyQt6 import QtCore, QtGui, QtWidgets

from plug_qt import vimo

class OverlayView(
        vimo.View, 
        QtWidgets.QWidget
        ):

    def __init__(
        self,
        *args,
        view=None,
        objectName="Overlay",
        **kwargs,
    ):
        self.dark = True
        self.blur = False
        self.current = None
        self.previous = None
        self.activated = True
        self.views={}
        self.m_view = view 
        super().__init__(*args, objectname=objectName, **kwargs)
        self.setPalette(
            QtGui.QPalette(QtCore.Qt.GlobalColor.transparent))
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.resized.connect(self.updateOverlayPosition)
        self.setupUI()
        self.hide()

    def setup(self):
        super().setup()
        if self.m_view:
            self.setParent(self.m_view)
            self.m_view.resized.connect(
                    self.updateOverlaySize)

    def updateOverlaySize(self, view):
        self.resize(view.size())

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

    def addView(self, view, **kwargs):
        view.setParent(self)
        view.setManager(self)
        self.views[id(view)] = view

    def removeView(self, view, **kwargs):
        self.hide()
        view.setManager()
        view.setParent(None)
        self.m_blur = self.blur
        self.views.pop(id(view))

    def betView(self, view, **kwargs):
        view.hide()
        self.m_blur = False
        self.m_dark = False
        self.app.view.update()
        rec = kwargs.get("recursive")
        if rec:
            self.octivate()

    def setView(
        self,
        view=None,
        blur=False,
        dark=True,
        active_views=[],
        **kwargs,
    ):
        for v in self.views.values():
            if v in active_views:
                continue
            if v == view:
                continue
            v.hide()
        self.m_blur = blur
        self.m_dark = dark
        c, p = view, self.current
        self.current, self.previous = c, p
        self.show()
        view.show(**kwargs)
        view.setFocus()
        self.app.view.update()

    def updateOverlayPosition(self):
        self.resized.disconnect(
                self.updateOverlayPosition)
        geometry = self.geometry()
        self.setGeometry(geometry)
        self.resized.connect(self.updateOverlayPosition)

    def activate(self, *args, **kwargs):
        pass

    def insertView(self, idx, view, **kwargs):
        pass
