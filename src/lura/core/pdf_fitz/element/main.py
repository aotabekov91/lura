import fitz
from PyQt6 import QtCore, QtGui

import plug

from . import mixin


class FitzElement(
    mixin.Block,
    mixin.Search,
    mixin.Normed,
    mixin.Annotate,
    plug.element.Element,
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
        xpos,
        ypos,
        rotation,
        pixel,
        clip=None,
        alpha=False,
        image_format=QtGui.QImage.Format.Format_RGB888,
    ):
        matrix = fitz.Matrix(xpos, ypos)
        if rotation:
            matrix.prerotate(rotation % 360)
        pixmap = self.m_data.get_pixmap(
                clip=clip, 
                alpha=alpha, 
                matrix=matrix,
        )

        img = QtGui.QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            image_format,
        )
        img.setDevicePixelRatio(pixel)
        return img
