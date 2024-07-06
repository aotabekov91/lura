from PyQt6 import QtCore, QtWidgets

from plug_qt import vimo


class OverlayGraphicsView(
    vimo.View,
    QtWidgets.QGraphicsView,
):
    def setup(self):
        super().setup()
        self.setupUI()
        self.w_ratio = 1.0
        self.h_ratio = 1.0
        self.current = None
        self.hide()
        self.resized.connect(self.updateView)

    def setupUI(self):
        self.m_scene = QtWidgets.QGraphicsScene()
        self.setScene(self.m_scene)

    def updatePosition(self):
        r = self.parent().rect()
        self.setGeometry(r)

    def setView(
        self,
        *args,
        view=None,
        **kwargs,
    ):
        self.updatePosition()
        s = self.size()
        self.m_scene.addItem(view)
        sw = s.width() - 20
        sh = s.height() - 20
        g = QtCore.QRectF(0, 0, sw, sh)
        view.resize(QtCore.QSizeF(sw, sh))
        view.setGeometry(g)
        self.centerOn(view)
        self.current = view

    def updateView(self):
        if self.current:
            self.centerOn(self.current)

    def removeView(self, v):
        self.m_scene.removeItem(v)
