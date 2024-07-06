from PyQt6 import QtCore, QtGui

from ..layout import Layout
from .utils import BaseScene


class Scene(Layout):
    hasScene = True
    scene_color = "black"
    scene_class = BaseScene

    def setup(self):
        self.m_scene = None
        self.setupScene()
        super().setup()

    def setupScene(self):
        if self.scene_class:
            s = self.scene_class()
            self.m_scene = s
            self.setScene(s)
            if self.scene_color:
                c = QtGui.QColor(self.scene_color)
                s.setBackgroundBrush(c)

    def clearScene(self):
        self.m_scene.clear()

    def updateLayout(self):
        y = 0.0
        x, r, h = self.m_layout.load(self.m_items)
        w = r - x
        self.m_scene.setSceneRect(x, y, w, h)
        self.setSceneRect(QtCore.QRectF(x, y, w, h))
