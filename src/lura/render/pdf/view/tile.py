from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .task import Task

class Tile(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self.m_parent=parent
        self.m_rect = QRect()
        self.m_cropRect = QRectF() 
        self.m_pixmapError = False
        self.m_pixmap = QPixmap()
        self.m_obsoletePixmap = QPixmap()
        self.s_cache=parent.s_cache
        self.setup()

    def pageItem(self): return self.m_parent

    def setup(self):

        self.m_renderTask = Task(self)
        self.m_renderTask.finished.connect(
            self.on_renderTask_finished)
        self.m_renderTask.imageReady.connect(
            self.on_renderTask_imageReady)
        self.m_renderTask.cancel(True)
        self.m_renderTask.wait()

    def on_renderTask_imageReady(self, rect, prefetch, image):

        if image is None:
            self.m_pixmapError=True
            return
        if self.m_rect==rect:

            self.m_obsoletePixmap=QPixmap()
            if prefetch and not self.m_renderTask.wasCanceledForcibly():
                self.s_cache[self.cacheKey()]=QPixmap.fromImage(image)
            elif not self.m_renderTask.wasCanceled():
                # image=self.revert(image)
                self.m_pixmap=QPixmap.fromImage(image)

    def revert(self, image):

        # todo: very slow
        for y in range(image.height()):
            for x in range(image.width()):

                pc=image.pixel(x, y)
                red=abs(255-qRed(pc))
                green=abs(255-qGreen(pc))
                blue=abs(255-qBlue(pc))
                c=[red, green, blue]
                if c!=[0, 0, 0]: c=[124, green, 0]
                nc=QColor(*c).rgb()
                image.setPixel(x, y, nc)
        return image

    def takePixmap(self):
        key = self.cacheKey()
        pixmap = self.s_cache.get(key)

        if self.isNotEmptyPixmap(pixmap):
            self.m_obsoletePixmap = QPixmap() 
            return pixmap

        elif self.isNotEmptyPixmap(self.m_pixmap):
            self.s_cache[key]=self.m_pixmap
            pixmap = self.m_pixmap
            self.m_pixmap = QPixmap() 
            return pixmap
        else:
            self.startRender()

    def refresh(self, dropCachedPixmap=False):
        if not dropCachedPixmap:
            object_ = self.s_cache.get(self.cacheKey())
            if object_ is not None:
                self.m_obsoletePixmap = object_
        else:
            key=self.cacheKey()
            if key in self.s_cache:
                self.s_cache.pop(key)
            self.m_obsoletePixmap = QPixmap() 

        self.m_renderTask.cancel(True)
        self.m_pixmapError = False
        self.m_pixmap =QPixmap()

    def startRender(self, prefetch=False):
        cond = self.m_pixmapError or self.m_renderTask.isRunning()
        cond = cond or (prefetch and self.cacheKey() in self.s_cache)
        if cond: return

        self.m_renderTask.start(self.m_rect, prefetch)

    def cancelRender(self):
        self.m_renderTask.cancel()
        self.m_pixmap=QPixmap()
        self.m_obsoletePixmap=QPixmap()

    def deleteAfterRender(self):
        self.cancelRender()
        if not self.m_renderTask.isRunning():
            del self

    def on_renderTask_finished(self):
        self.pageItem().update()

    def cacheKey(self):
        page = self.pageItem()
        size=self.m_rect

        data = (
            self.pageItem().xresol(),
            self.pageItem().yresol(),
            self.pageItem().scale(),
            (size.x(), size.y(), size.width(), size.height()),
        )
        return (page, data)

    def rect(self):
        return self.m_rect

    def setRect(self, rect):
        self.m_rect = rect

    def dropPixmap(self):
        self.m_pixmap = None 

    def dropObsoletePixmap(self):
        self.m_obsoletePixmap = None 

    def dropCachedPixmaps(self, page):

        for key, pixmap in list(self.s_cache.items()):
            if key[0]==page: self.s_cache.pop(key)

    def paint(self, painter, topLeft):

        pixmap = self.takePixmap()
        if self.isNotEmptyPixmap(pixmap):
            painter.drawPixmap(
                    self.m_rect.topLeft()+topLeft, 
                    pixmap)
        elif self.isNotEmptyPixmap(self.m_obsoletePixmap):
            painter.drawPixmap(
                    QRectF(self.m_rect).translated(topLeft), 
                    self.m_obsoletePixmap, 
                    QRectF())
        else:
            if not self.m_pixmapError:
                return
            else:
                raise

    def isNotEmptyPixmap(self, pixmap):
        if pixmap is not None:
            if pixmap!=QPixmap(): 
                size=pixmap.size()
                if size.width()*size.height()>0: 
                    return True
        else:
            return False
