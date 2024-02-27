from gizmo.utils import tag
from PyQt5 import QtCore, QtGui


class Resize:
    rubberbandIncrement = 0.05

    @tag("G", modes=["visual[band]|^own"])
    def setBandCorner(self, rstart=None, **kwargs):
        if rstart == 1:
            self.m_band_corner = "topLeft"
        elif rstart == 2:
            self.m_band_corner = "topRight"
        elif rstart == 3:
            self.m_band_corner = "bottomRight"
        else:
            self.m_band_corner = "bottomLeft"
        i = self.m_band["item"]
        i.refresh()

    @tag("l", modes=["visual[band]|^own"])
    def bandVisualGoToRight(self, rstart=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = self.rubberbandIncrement * rstart
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "bottomLeft"]:
            b.setX(b.x() + delta)
        else:
            b.setWidth(b.width() + delta)
        i.refresh()

    @tag("h", modes=["visual[band]|^own"])
    def bandVisualGoToLeft(self, rstart=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = -self.rubberbandIncrement * rstart
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "bottomLeft"]:
            b.setX(b.x() + delta)
        else:
            b.setWidth(b.width() + delta)
        i.refresh()

    @tag("k", modes=["visual[band]|^own"])
    def bandVisualGoToUp(self, rstart=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = -self.rubberbandIncrement * rstart
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "topRight"]:
            b.setY(b.y() + delta)
        else:
            b.setHeight(b.height() + delta)
        i.refresh()

    @tag("j", modes=["visual[band]|^own"])
    def bandVisualGoToDown(self, rstart=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = self.rubberbandIncrement * rstart
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "topRight"]:
            b.setY(b.y() + delta)
        else:
            b.setHeight(b.height() + delta)
        i.refresh()
