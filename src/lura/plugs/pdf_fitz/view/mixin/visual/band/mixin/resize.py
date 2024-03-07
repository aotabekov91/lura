from gizmo.utils import tag
from PyQt5 import QtCore, QtGui


class Resize:
    rubberbandIncrement = 0.05

    @tag("G(visual[band])[^]")
    def setBandCorner(self, xrange=None, **kwargs):
        if xrange == 1:
            self.m_band_corner = "topLeft"
        elif xrange == 2:
            self.m_band_corner = "topRight"
        elif xrange == 3:
            self.m_band_corner = "bottomRight"
        else:
            self.m_band_corner = "bottomLeft"
        i = self.m_band["item"]
        i.refresh()

    @tag("l(visual[band])[^]")
    def bandVisualGoToRight(self, xrange=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = self.rubberbandIncrement * xrange
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "bottomLeft"]:
            b.setX(b.x() + delta)
        else:
            b.setWidth(b.width() + delta)
        i.refresh()

    @tag("h(visual[band])[^]")
    def bandVisualGoToLeft(self, xrange=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = -self.rubberbandIncrement * xrange
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "bottomLeft"]:
            b.setX(b.x() + delta)
        else:
            b.setWidth(b.width() + delta)
        i.refresh()

    @tag("k(visual[band])[^]")
    def bandVisualGoToUp(self, xrange=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = -self.rubberbandIncrement * xrange
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "topRight"]:
            b.setY(b.y() + delta)
        else:
            b.setHeight(b.height() + delta)
        i.refresh()

    @tag("j(visual[band])[^]")
    def bandVisualGoToDown(self, xrange=1, **kwargs):
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        r = self.rubberbandIncrement * xrange
        delta = min(b.y(), b.height()) * r
        if self.m_band_corner in ["topLeft", "topRight"]:
            b.setY(b.y() + delta)
        else:
            b.setHeight(b.height() + delta)
        i.refresh()
