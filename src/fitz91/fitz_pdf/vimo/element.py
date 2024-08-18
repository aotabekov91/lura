import fitz
from PyQt6 import QtCore, QtGui

import plug

class FitzElement(
    plug.element.Element,
    QtCore.QObject,
):
    functors={}
    dataUpdated = QtCore.pyqtSignal()
    dataChanged = QtCore.pyqtSignal()
    repaintWanted = QtCore.pyqtSignal()

    def setup(self):
        self.setSize()
        super().setup()
        size = self.size()
        self.m_norm = QtGui.QTransform()
        self.m_norm.scale(size.width(), size.height())

    @classmethod
    def addFunctor(cls, name, functor):
        if not name in cls.functors:
            cls.functors[name]=[]
        cls.functors[name]+=[functor]

    @classmethod
    def getFunctor(cls, name):
        return cls.functors.get(name, [])

    def unify(self, point):
        norm = self.m_norm.inverted()[0]
        if type(point) == tuple:
            if len(point) == 2:
                point = QtCore.QPointF(*point)
            elif len(point) == 4:
                point = QtCore.QRectF(*point)
        if type(point) in [QtCore.QPoint, QtCore.QPointF]:
            u = norm.map(point)
        else:
            p = point.normalized()
            u = norm.mapRect(p)
        return u

    def unity(self, point):
        norm = self.m_norm
        if type(point) == tuple:
            if len(point) == 2:
                point = QtCore.QPointF(*point)
            elif len(point) == 4:
                point = QtCore.QRectF(*point)
        if type(point) in [QtCore.QPoint, QtCore.QPointF]:
            u = norm.map(point)
        else:
            p = point.normalized()
            u = norm.mapRect(p)
        return u

    def setSize(self):
        b = self.m_data.bound()
        w, h = b.width, b.height
        self.m_size = QtCore.QSizeF(w, h)

    def size(self):
        return self.m_size

    def renderMatrix(self, data):
        xpos=data.get('xpos', None)
        ypos=data.get('xpos', None)
        matrix = fitz.Matrix(xpos, ypos)
        for functor in self.getFunctor('renderMatrix'):
            matrix=functor(data, matrix)
        return matrix

    def renderImage(self, data):
        pixel=data.get('pixel')
        clip=data.get('clip', False)
        alpha=data.get('alpha', False)
        image_format=data.get(
                'image_format', 
                QtGui.QImage.Format.Format_RGB888)
        matrix=self.renderMatrix(data)
        pixmap = self.m_data.get_pixmap(
                clip=clip, 
                alpha=alpha, 
                matrix=matrix)
        img = QtGui.QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            image_format)
        img.setDevicePixelRatio(pixel)
        for functor in self.getFunctor('renderImage'):
            img=functor(data, img)
        return img
