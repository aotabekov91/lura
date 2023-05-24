from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .rendertask import RenderTask

class TileItem(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self.m_rect = QRect()
        self.m_cropRect = QRectF() 
        self.m_pixmapError = False
        self.m_pixmap = QPixmap()
        self.m_obsoletePixmap = QPixmap()
        self.s_cache=parent.s_cache
        self.s_settings=parent.s_settings
        self.setup()

    def setup(self):
        self.m_renderTask = RenderTask(
                self.parentPage().m_page, self)

        self.m_renderTask.finished.connect(
            self.on_renderTask_finished)
        self.m_renderTask.imageReady.connect(
            self.on_renderTask_imageReady)

        self.m_renderTask.cancel(True)
        self.m_renderTask.wait()

    def on_renderTask_imageReady(self, settings, rect, prefetch, image):

        if self.parentPage().s_settings!=settings or self.m_rect!=rect:
            return

        self.m_obsoletePixmap=QPixmap()

        if image is None:
            self.m_pixmapError=True
            return

        if prefetch and not self.m_renderTask.wasCanceledForcibly():

            self.s_cache[self.cacheKey()]=QPixmap.fromImage(image)

        elif not self.m_renderTask.wasCanceled():

            self.m_pixmap=QPixmap.fromImage(image)

    def parentPage(self):
        return self.parent()

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
        self.m_renderTask.start(
            self.parentPage().s_settings,
            self.m_rect, prefetch)

    def cancelRender(self):
        self.m_renderTask.cancel()
        self.m_pixmap=QPixmap()
        self.m_obsoletePixmap=QPixmap()

    def deleteAfterRender(self):
        self.cancelRender()
        if not self.m_renderTask.isRunning():
            del self

    def on_renderTask_finished(self):
        self.parentPage().update()

    # def rect(self, renderParam, rect, prefetch, image, cropRect):
    #     raise

    def cacheKey(self):
        page = self.parentPage()

        size=self.m_rect
        s=(size.x(), size.y(), size.width(), size.height()),

        data = (
            self.s_settings['resolution']['resolutionX'],
            self.s_settings['resolution']['resolutionY'],
            self.s_settings['scaleFactor'],
            s
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
