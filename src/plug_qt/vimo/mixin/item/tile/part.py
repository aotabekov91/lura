from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap

from .task import Task


class Part(QtCore.QObject):
    cropRectChanged = QtCore.pyqtSignal()

    def __init__(self, item):
        self.m_item = item
        self.m_error = False
        self.m_elem = item.element()
        self.m_rect = QtCore.QRect()
        self.m_pixmap = QPixmap()
        self.m_cropRect = QtCore.QRectF()
        self.m_obsoletePixmap = QPixmap()
        super().__init__(item)
        self.setup()

    def setup(self):
        self.m_elem.addCache("pixmap")
        self.m_runner = Task(self)
        self.m_runner.finished.connect(
            self.on_renderTask_finished
        )
        self.m_runner.imageReady.connect(
            self.on_renderTask_imageReady
        )
        self.m_runner.cancel(True)
        self.m_runner.wait()

    def on_renderTask_imageReady(self, rect, prefetch, img):
        if img is None:
            self.m_error = True
            return
        if self.m_rect == rect:
            self.m_obsoletePixmap = QPixmap()
            c = self.m_runner.wasCanceled()
            f = self.m_runner.wasCanceledForcibly()
            if prefetch and not f:
                k = self.getCacheKey()
                p = QPixmap.fromImage(img)
                self.setCache(k, p)
            elif not c:
                pmap = QPixmap.fromImage(img)
                self.m_pixmap = pmap

    def takePixmap(self):
        k = self.getCacheKey()
        pmap = self.getCache(k)

        if self.isNotEmptyPixmap(pmap):
            self.m_obsoletePixmap = QPixmap()
            return pmap
        elif self.isNotEmptyPixmap(self.m_pixmap):
            self.setCache(k, self.m_pixmap)
            pmap = self.m_pixmap
            self.m_pixmap = QPixmap()
            return pmap
        else:
            self.startRender()

    def refresh(self, dropCache=False):
        if not dropCache:
            k = self.getCacheKey()
            obj = self.getCache(k)
            if obj:
                self.m_obsoletePixmap = obj
        else:
            self.resetCache()
            self.m_obsoletePixmap = QPixmap()
        self.m_error = False
        self.m_runner.cancel(True)
        self.m_pixmap = QPixmap()

    def startRender(self, prefetch=False):
        if self.m_error:
            return
        elif self.m_runner.isRunning():
            return
        k = self.getCacheKey()
        c = self.getCache(k)
        if prefetch and c:
            return
        self.m_runner.start(self.m_rect, prefetch)

    def cancelRender(self):
        self.m_runner.cancel()
        self.m_pixmap = QPixmap()
        self.m_obsoletePixmap = QPixmap()

    def deleteAfterRender(self):
        self.cancelRender()
        if not self.m_runner.isRunning():
            del self

    def on_renderTask_finished(self):
        self.m_item.update()

    def getCacheKey(self):
        s = self.m_rect
        i = self.m_item
        pos = s.x(), s.y(), s.width(), s.height()
        d = i.index(), i.xresol, i.yresol, i.m_scale
        return (pos, d)

    def setCache(self, key, value):
        self.m_elem.setCache(key, value, "pixmap")

    def getCache(self, key):
        return self.m_elem.getCache(key, "pixmap")

    def resetCache(self):
        self.m_elem.clearCache("pixmap")

    def dropCache(self, key):
        self.m_elem.dropCache(key, "pixmap")

    def rect(self):
        return self.m_rect

    def setRect(self, rect):
        self.m_rect = rect

    def dropPixmap(self):
        self.m_pixmap = None

    def dropObsoletePixmap(self):
        self.m_obsoletePixmap = None

    def dropCaches(self, page):
        self.resetCache()

    def paint(self, p, topLeft):
        pmap = self.takePixmap()
        if self.isNotEmptyPixmap(pmap):
            p.drawPixmap(
                self.m_rect.topLeft() + topLeft,
                pmap,
            )
        elif self.isNotEmptyPixmap(self.m_obsoletePixmap):
            # p=QtCore.QRectF(self.m_rect).translated(topLeft)
            r = QtCore.QRectF(self.m_rect).translated(
                topLeft
            )
            p.drawPixmap(
                r,
                self.m_obsoletePixmap,
                QtCore.QRectF(),
            )

    def isNotEmptyPixmap(self, pixmap):
        if pixmap is not None:
            if pixmap != QPixmap():
                size = pixmap.size()
                if size.width() * size.height() > 0:
                    return True
