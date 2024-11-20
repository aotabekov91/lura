from PyQt6 import QtCore, QtGui, QtWidgets

from plug_qt import vimo

class OverlayView(
        vimo.View, 
        QtWidgets.QWidget
        ):

    def __init__(self, *args, view=None, **kwargs):
        self.m_view = view 
        super().__init__(*args, **kwargs)

    def setup(self):
        super().setup()
        self.dark = True
        self.blur = False
        if self.m_view:
            self.setParent(self.m_view)
            self.m_view.resized.connect(
                    self.updateOverlaySize)
        self.setPalette(
            QtGui.QPalette(QtCore.Qt.GlobalColor.transparent))
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.resized.connect(self.updateOverlayPosition)
        self.setupUI()
        self.hide()

    def updateOverlaySize(self, view):
        self.resize(view.size())

    def setupUI(self):
        self.m_blur = self.blur
        self.m_dark = self.dark
        config = self.app.m_config.get(
                self.name, {})
        self.m_config.update(config)
        blur_color = self.m_config.get(
            "blur_color", (25, 25, 25, 200))
        dark_color = self.m_config.get(
            "dark_color", "black")
        self.blur_color = QtGui.QColor(*blur_color)
        self.dark_color = QtGui.QColor(dark_color)

    def addView(self, view, **kwargs):
        view.setParent(self)
        view.setManager(self)

    def removeView(self, view, **kwargs):
        self.hide()
        view.setManager()
        view.setParent(None)
        self.m_blur = self.blur

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
        **kwargs,
    ):

        self.m_blur = blur
        self.m_dark = dark
        self.show()
        view.show(**kwargs)
        view.setFocus()
        self.app.view.update()

    def updateOverlayPosition(self):
        self.resized.disconnect(
                self.updateOverlayPosition)
        geometry = self.geometry()
        self.setGeometry(geometry)
        self.resized.connect(
                self.updateOverlayPosition)

    def activate(self, *args, **kwargs):
        pass

    def insertView(self, idx, view, **kwargs):
        pass

