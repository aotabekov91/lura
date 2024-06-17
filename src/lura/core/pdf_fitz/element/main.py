import fitz
from PyQt6 import QtCore, QtGui
from lura import gizmo

from . import mixin


class FitzElement(
    mixin.Trim,
    mixin.Block,
    mixin.Links,
    mixin.Search,
    mixin.Normed,
    mixin.Annotate,
    gizmo.ui.core.element.Element,
    QtCore.QObject,
):
    dataUpdated = QtCore.pyqtSignal()
    dataChanged = QtCore.pyqtSignal()
    repaintWanted = QtCore.pyqtSignal()

    def setup(self):
        self.setSize()
        super().setup()

    def setSize(self):
        b = self.m_data.bound()
        w, h = b.width, b.height
        self.m_size = QtCore.QSizeF(w, h)

    def size(self):
        return self.m_size

    def render(self, data, **kwargs):
        return self.m_model.getPixmapCache(self.index(), data)

    def renderImage(
        self,
        idx,
        x,
        y,
        scale,
        rotation,
        pratio,
        grayScale,
        clip,
        trim,
    ):
        matrix = fitz.Matrix(x, y)
        if rotation:
            matrix.prerotate(rotation % 360)
        p = self.m_data.get_pixmap(
            clip=clip,
            alpha=False,
            # colorspace='rgb',
            matrix=matrix,
        )

        img = QtGui.QImage(
            p.samples,
            p.width,
            p.height,
            p.stride,
            QtGui.QImage.Format.Format_RGB888,
        )
        img.setDevicePixelRatio(pratio)
        if grayScale:
            img.invertPixels()
        return img
