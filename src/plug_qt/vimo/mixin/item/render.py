from math import floor
from plug.utils import hashdict

from PyQt6 import QtCore, QtGui

class Render:
    canRender = True
    painted = QtCore.pyqtSignal(
        object, object, object, object
    )

    def setElement(self, elem):
        super().setElement(elem)
        if elem:
            self.m_size = elem.size()
            self.redraw()

    def setup(self):
        super().setup()
        v = self.m_kwargs
        self.m_cache_key = None
        self.m_rect = QtCore.QRectF()
        self.m_brect = QtCore.QRectF()
        self.m_size = self.m_rect.size()
        self.m_trans = QtGui.QTransform()
        self.scale = v.get("scale", 1.0)
        self.xresol = v.get("xresol", 72.0)
        self.yresol = v.get("yresol", 72.0)
        self.m_rotation = v.get("rotation", None)
        self.tileSize = v.get("tileSize", 1024)
        self.devicePixelRatio = v.get("devicePixelRatio", 1)
        self.m_view.pixmapReady.connect(self.setPixmap)
        self.m_view.repaintWanted.connect(self.refresh)
        self.prepareGeometry()

    def setRotation(self, rotation=None):
        self.m_rotation = rotation
        self.redraw()

    def rotation(self):
        return self.m_rotation

    def paint(self, p, o, w):
        pixmap = self.takePixmap()
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
            p.setRenderHints(opt)
            pos = self.m_brect.topLeft()
            p.drawPixmap(pos, pixmap)
            self.painted.emit(p, o, w, self)

    def takePixmap(self):
        if not self.m_cache_key:
            self.updateCacheKey()
        data = self.m_element.render(self.m_cache_key)
        if data:
            return data[-1]

    def updateCacheKey(self):
        rs = self.m_brect.size()
        os = self.m_element.size()
        xpos = rs.width() / os.width()
        ypos = rs.height() / os.height()
        xpos = round(xpos, 3)
        ypos = round(ypos, 3)
        rotation = self.m_rotation
        idx = self.m_element.index()
        pixel = self.devicePixelRatio
        self.m_cache_key=hashdict(
                idx=idx,
                xpos=xpos,
                ypos=ypos,
                rotation=rotation,
                pixel=pixel)

    def setPixmap(self, idx, data, pixmap):
        c1 = self.index() == idx
        c2 = data == self.m_cache_key
        if c1 and c2:
            self.refresh()

    def refresh(self):
        if self.scene():
            self.scene().update()
        else:
            self.update()

    def redraw(self):
        self.prepareGeometryChange()
        self.updateTransformation()
        self.prepareGeometry()
        self.updateCacheKey()
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
        x = self.xresol * self.scale / 72.0
        y = self.yresol * self.scale / 72.0
        self.m_trans.scale(x, y)

    def prepareGeometry(self):
        s = self.size()
        p = QtCore.QPointF()
        r = QtCore.QRectF(p, s)
        r = self.m_trans.mapRect(r)
        r.setWidth(floor(r.width()))
        r.setHeight(floor(r.height()))
        self.setBoundingRect(r)

    def mapToElement(self, p, unify=True):
        e = self.m_element
        t = self.m_trans.inverted()[0]
        p = self.getPolygon(p)
        if type(p) in [
            QtCore.QPoint,
            QtCore.QPointF,
        ]:
            p = t.map(p)
        else:
            p = t.mapRect(p)
        if unify:
            p = e.unify(p)
        return p

    def mapToItem(self, p, unified=False):
        t = self.m_trans
        e = self.m_element
        p = self.getPolygon(p)
        if unified:
            p = e.unity(p)
        if type(p) in [
            QtCore.QPoint,
            QtCore.QPointF,
        ]:
            return t.map(p)
        else:
            return t.mapRect(p)

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
