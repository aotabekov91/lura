import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .tileitem import TileItem

class PageItem(QGraphicsObject):

    cropRectChanged = pyqtSignal()
    linkClicked = pyqtSignal(bool, int, float, float)
    wasModified = pyqtSignal()
    mouseDoubleClick=pyqtSignal(int, 'QPointF')

    mouseReleaseEventOccured=pyqtSignal(object, object)
    mouseMoveEventOccured=pyqtSignal(object, object)
    mousePressEventOccured=pyqtSignal(object, object)
    mouseDoubleClickOccured=pyqtSignal(object, object)

    hoverMoveEventOccured=pyqtSignal(object, object)
    pageHasBeenJustPainted=pyqtSignal(object, object, object, object)

    def __init__(self, page, view):
        super().__init__(objectName='pageItem')
        self.m_page = page
        self.m_size = page.size()
        self.m_view=view
        self.m_transform = QTransform()
        self.m_normalizedTransform = QTransform()
        self.m_boundingRect = QRectF() 
        self.m_menu=QMenu(view)
        self.s_cache=view.s_cache
        self.setAcceptHoverEvents(True)

        self.m_scaleFactor=self.view().settings().getfloat('scaleFactor', 1.)
        self.m_rotation=self.view().settings().getint('rotation', 0)
        self.m_xresol=self.view().settings().getint('resolutionX', 72)
        self.m_yresol=self.view().settings().getint('resolutionY', 72)
        self.m_proxy_padding=self.view().settings().getfloat('proxyPadding', 6.)
        self.m_device_pixel_ration=self.view().settings().getfloat('devicePixelRatio', 1.)
        self.m_use_tiling=self.view().settings().getboolean('useTiling', False)

        self.setup()

    def setup(self):
        if not self.m_use_tiling: 
            tile=TileItem(self)
            self.m_tileItems=[tile]
        self.redraw()

    def boundingRect(self):
        self.prepareGeometry()
        return self.m_boundingRect

    def paint(self, painter, options, widgets):
        painter.setRenderHint(QPainter.Antialiasing)

        self.paintPage(painter, options.exposedRect)
        # self.paintHighlight(painter, options, widgets)

        self.pageHasBeenJustPainted.emit(painter, options, widgets, self)

    def paintPage(self, painter, exposedRect):
        painter.fillRect(self.m_boundingRect, QBrush(QColor('white')))
        self.m_tileItems[0].paint(painter, self.m_boundingRect.topLeft())

    def setResolution(self, resolutionX, resolutionY):
        cond=self.xresol() != resolutionX or self.yresol() != resolutionY
        if cond and (resolutionY>0 and resolutionX>0):

            self.refresh()

            self.setXResol(resolutionX)
            self.setYResol(resolutionY)

            self.redraw()

    def setScaleFactor(self, scaleFactor):
        self.m_scaleFactor=scaleFactor
        self.redraw(refresh=True)

    def redraw(self, refresh=False):
        if refresh: self.refresh()
        self.prepareGeometryChange()
        self.prepareGeometry()

    def proxyPadding(self):
        return self.m_proxy_padding

    def scale(self):
        return self.m_scaleFactor

    def rotation(self):
        return self.m_rotation

    def setRotation(self, rotation):
        self.m_rotation=rotation

    def devicePixelRatio(self):
        return self.m_device_pixel_ration

    def xresol(self):
        return self.m_xresol 

    def setXResol(self, xresol):
        self.m_xresol=xresol

    def yresol(self):
        return self.m_yresol

    def setYResol(self, yresol):
        self.m_yresol=yresol

    def prepareGeometry(self):
        self.m_transform.reset()
        xScale = self.xresol()*self.scale()/72.
        yScale = self.yresol()*self.scale()/72.
        self.m_transform.scale(xScale, yScale)

        self.m_normalizedTransform.reset()
        self.m_normalizedTransform.scale(xScale, yScale)
        self.m_normalizedTransform.scale(
            self.m_size.width(), self.m_size.height())

        self.m_boundingRect=self.m_transform.mapRect(
                QRectF(QPointF(), self.m_size))

        self.m_boundingRect.setWidth(math.floor(
            self.m_boundingRect.width()))
        self.m_boundingRect.setHeight(math.floor(
            self.m_boundingRect.height()))

        self.prepareTiling()

    def prepareTiling(self):
        rect=QRect(0, 0, int(self.m_boundingRect.width()), int(self.m_boundingRect.height()))
        self.m_tileItems[0].setRect(rect)

    def size(self):
        return self.m_size

    def displayedWidth(self):
        return (self.xresol()/72.0)*self.m_size.width()

    def displayedHeight(self):
        return (self.yresol()/72.0)*self.m_size.height()


    def refresh(self, dropCachedPixmap=False):
        for tile in self.m_tileItems:
            tile.refresh(dropCachedPixmap)
            if dropCachedPixmap: tile.dropCachedPixmaps(self)
        self.update()

    def startRender(self, prefetch):
        for tile in self.m_tileItems:
            tile.startRender(prefetch)

    def cancelRender(self):
        for tile in self.m_tileItems:
            tile.cancelRender()

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickOccured.emit(event, self)

    def mousePressEvent(self, event):
        self.mousePressEventOccured.emit(event, self)

    def mouseMoveEvent(self, event):
        self.mouseMoveEventOccured.emit(event, self)

    def mouseReleaseEvent(self, event):
        self.mouseReleaseEventOccured.emit(event, self)

    def mapToPage(self, polygon):
        if type(polygon) in [QPoint, QPointF]:
            ununified=self.m_transform.inverted()[0].map(polygon)
            unified=self.m_normalizedTransform.inverted()[0].map(polygon)
        else:
            polygon=polygon.normalized()
            ununified=self.m_transform.inverted()[0].mapRect(polygon)
            unified=self.m_normalizedTransform.inverted()[0].mapRect(polygon)
        return ununified, unified

    def mapToItem(self, polygon):
        if type(polygon) in [QPoint, QPointF]:
            ununified=self.m_transform.map(polygon)
            unified=self.m_normalizedTransform.map(polygon)
        else:
            polygon=polygon.normalized()
            ununified=self.m_transform.mapRect(polygon)
            unified=self.m_normalizedTransform.mapRect(polygon)
        return ununified, unified

    def setActions(self, actions):
        self.m_menu.clear()
        for action in actions:
            self.m_menu.addAction(action)

    def hoverMoveEvent(self, event):
        self.hoverMoveEventOccured.emit(event, self)

    def showOverlay(self, overlay, hideOverlay, elements, selectedElement):
        for element in elements:
            if not element in overlay:
                self.addProxy(overlay, hideOverlay, element)
            if element==selectedElement:
                overlay[element].widget().setFocus()

    def hideOverlay(self, overlay, deleteLater=False):
        discardedOverlay=Overlay()
        discardedOverlay.swap(overlay)
        if not discardedOverlay.isEmpty():
            for i in range(discardedOverlay.constEnd()):
                if deleteLater:
                    raise
            self.refresh()

    def addProxy(self, position, widget, hideOverlay):
        proxy=QGraphicsProxyWidget(self)
        proxy.setWidget(widget)
        widget.setFocus()
        proxy.setAutoFillBackground(True)
        self.setProxyGeometry(position, proxy)
        proxy.visibleChanged.connect(hideOverlay)

    def setProxyGeometry(self, position, proxy):
        width=proxy.preferredWidth()
        height=proxy.preferredHeight()
        x=position.x()-0.5*proxy.preferredWidth()
        y=position.y()-0.5*proxy.preferredHeight()

        proxyPadding=self.proxyPadding()

        x=max([x, self.m_boundingRect.left()+proxyPadding])
        y=max([y, self.m_boundingRect.top()+ proxyPadding])
        width=min([width, self.m_boundingRect.right()-proxyPadding-x])
        height=min([height, self.m_boundingRect.bottom()-y])

        proxy.setGeometry(QRectF(x, y, width, height))

    def scaledResolutionX(self):
        return self.scale()*self.devicePixelRatio()*self.xresol()

    def scaledResolutionY(self):
        return self.scale()*self.devicePixelRatio()*self.yresol()

    def page(self):
        return self.m_page

    def view(self):
        return self.m_view
