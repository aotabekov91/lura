from math import floor

from PyQt6 import QtCore, QtGui, QtWidgets

from plug import hashdict
from plug_qt.vimo.item import Item

class FitzItem(Item, QtWidgets.QGraphicsObject):

    painted = QtCore.pyqtSignal(
        object, object, object, object)

    def setup(self):
        self.m_key = hashdict()
        self.m_rect = QtCore.QRectF()
        self.m_brect = QtCore.QRectF()
        self.m_size = self.m_rect.size()
        self.m_trans = QtGui.QTransform()
        self.m_scale = self.m_kwargs.get(
                "scale", 1.0)
        self.xresol = self.m_kwargs.get(
                "xresol", 72.0)
        self.yresol = self.m_kwargs.get(
                "yresol", 72.0)
        self.tileSize = self.m_kwargs.get(
                "tileSize", 1024)
        self.devicePixelRatio = self.m_kwargs.get(
                "devicePixelRatio", 1)
        self.prepareGeometry()
        super().setup()

    def setElement(self, elem):
        super().setElement(elem)
        if elem:
            self.m_size = elem.size()
            self.redraw()

    def paint(self, painter, options, widget):
        pixmap = self.getPixmap()
        if pixmap:
            opt = QtGui.QPainter.RenderHint.Antialiasing
            opt = (
                opt
                | QtGui.QPainter.RenderHint.TextAntialiasing
            )
            opt = (
                opt
                | QtGui.QPainter.RenderHint.SmoothPixmapTransform
            )
            painter.setRenderHints(opt)
            pos = self.m_brect.topLeft()
            painter.drawPixmap(pos, pixmap)
            self.painted.emit(
                    painter, options, widget, self)

    def getPixmap(self):
        if not self.m_key:
            self.updateKey()
        model=self.m_element.model()
        data = model.getPixmap(self.m_element, self.m_key)
        if data:
            return data[-1]

    def getScale(self):
        return self.m_scale

    def setScale(self, scale):
        self.m_scale=scale
        self.redraw()

    def updateKey(self):
        rs = self.m_brect.size()
        os = self.m_element.size()
        xpos = rs.width() / os.width()
        ypos = rs.height() / os.height()
        self.m_key['xpos']=round(xpos, 3)
        self.m_key['ypos']=round(ypos, 3)
        self.m_key['idx']=self.m_element.index()
        self.m_key['pixel']=self.devicePixelRatio
        self.m_key['scale']=self.m_scale

    def setKey(self, name, value):
        self.m_key[name]=value

    def key(self, name):
        return self.m_key.get(name, None)

    def keys(self):
        return self.m_key

    def refresh(self):
        if self.scene():
            self.scene().update()
        else:
            self.update()

    def redraw(self):
        self.prepareGeometryChange()
        self.updateTransformation()
        self.prepareGeometry()
        self.updateKey()
        self.refresh()

    def size(self):
        return self.m_size

    def setResol(self, x, y):
        if y > 0 and x > 0:
            c1 = self.xresol != x
            c2 = self.yresol != y
            if c1 or c2:
                self.xresol = x
                self.yresol = y

    def displayedSize(self):
        s = self.m_size
        w, h = None, None
        if s:
            w = (self.xresol / 72.0) * s.width()
            h = (self.yresol / 72.0) * s.height()
        return w, h

    def updateTransformation(self):
        self.m_trans.reset()
        x = self.xresol * self.m_scale / 72.0
        y = self.yresol * self.m_scale / 72.0
        self.m_trans.scale(x, y)

    def prepareGeometry(self):
        size = self.size()
        point = QtCore.QPointF()
        rect = QtCore.QRectF(point, size)
        rect = self.m_trans.mapRect(rect)
        rect.setWidth(floor(rect.width()))
        rect.setHeight(floor(rect.height()))
        self.setBoundingRect(rect)

    def mapToElement(self, polygon, unify=True):
        inv_trans = self.m_trans.inverted()[0]
        polygon = self.getPolygon(polygon)
        if type(polygon) in [
            QtCore.QPoint,
            QtCore.QPointF,
        ]:
            polygon = inv_trans.map(polygon)
        else:
            polygon = inv_trans.mapRect(polygon)
        if unify:
            polygon = self.m_element.unify(polygon)
        return polygon

    def mapToItem(self, polygon, unified=False):
        polygon = self.getPolygon(polygon)
        if unified:
            polygon = self.m_element.unity(polygon)
        if type(polygon) in [
            QtCore.QPoint,
            QtCore.QPointF,
        ]:
            return self.m_trans.map(polygon)
        else:
            return self.m_trans.mapRect(polygon)

    def getPolygon(self, p):
        if type(p) == tuple:
            if len(p) == 2:
                p = QtCore.QPointF(*p)
            elif len(p) == 4:
                p = QtCore.QRectF(*p)
                p = p.normalized()
        return p

    def boundingRect(self):
        return self.m_brect

    def setBoundingRect(self, brect):
        self.m_brect = brect
