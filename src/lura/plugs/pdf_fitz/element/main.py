import fitz
import gizmo
from PyQt5 import QtCore, QtGui

from . import mixin

class FitzElement(
        mixin.Block,
        mixin.Links,
        mixin.Search,
        mixin.Annotate,
        mixin.TrimMargins,
        gizmo.vimo.element.Element, 
        QtCore.QObject
        ):

    dataUpdated=QtCore.pyqtSignal()
    repaintWanted=QtCore.pyqtSignal()

    def setup(self):

        super().setup()
        self.m_norm= QtGui.QTransform()
        self.fmt = QtGui.QImage.Format_RGB888
        self.setSize()
        self.updateTrans()
        
    def updateTrans(self):

        n=self.m_norm
        s=self.size()
        n.scale(s.width(), s.height())
        ninv=n.inverted()[0]
        self.m_norm_inv=ninv

    def setSize(self):

        b=self.m_data.bound()
        w, h = b.width, b.height
        self.m_size=QtCore.QSizeF(w, h)

    def size(self): 
        return self.m_size

    def render(self, data, **kwargs):

        return self.m_model.getPixmapCache(
                self.index(), data)

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

        matrix=fitz.Matrix(x, y)
        if rotation: 
            matrix.prerotate(rotation%360)
        p=self.m_data.get_pixmap(
                clip=clip,
                alpha=False,
                matrix=matrix,
                )
        img=QtGui.QImage(
            p.samples,
            p.width,
            p.height,
            p.stride,
            self.fmt)
        img.setDevicePixelRatio(pratio)
        if trim: 
            img=self.trimMargins(img) # todo
            raise
        if grayScale: img.invertPixels()
        return img
