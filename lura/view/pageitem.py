import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .cursor import Cursor
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

    def __init__(self, page, index, settings, document):
        super().__init__(objectName='pageItem')
        self.m_page = page
        self.m_size = page.size()
        self.m_index = index
        self.m_transform = QTransform()
        self.m_normalizedTransform = QTransform()
        self.m_boundingRect = QRectF() 
        self.m_menu=QMenu(document)
        self.m_cursor=Cursor(self)
        self.s_settings = settings
        self.s_cache=document.s_cache
        self.setup()

    def setup(self):
        self.highlightRect=None
        self.setAcceptHoverEvents(True)
        if not self.s_settings['pageItem']['useTiling']:
            tile=TileItem(self)
            self.m_tileItems=[tile]
        self.prepareGeometry()

    def boundingRect(self):
        self.prepareGeometry()
        return self.m_boundingRect

    def paint(self, painter, options, widgets):

        self.paintPage(painter, options.exposedRect)
        self.pageHasBeenJustPainted.emit(painter, options, widgets, self)
        self.highlight(painter, options, widgets)

    def paintPage(self, painter, exposedRect):
        painter.fillRect(self.m_boundingRect, QBrush(QColor('white')))
        self.m_tileItems[0].paint(painter, self.m_boundingRect.topLeft())

    def setResolution(self, resolutionX, resolutionY):

        resol = self.s_settings['resolution']
        cond=resol['resolutionX'] != resolutionX or resol['resolutionY'] != resolutionY

        if cond and (resolutionY>0 and resolutionX>0):

            self.refresh()

            self.s_settings['resolution']['resolutionX'] = resolutionX
            self.s_settings['resolution']['resolutionY'] = resolutionY

            self.prepareGeometryChange()
            self.prepareGeometry()

    def prepareGeometry(self):

        self.m_transform.reset()
        xScale = self.s_settings['resolution']['resolutionX'] * \
            self.s_settings['scaleFactor']/72.
        yScale = self.s_settings['resolution']['resolutionY'] * \
            self.s_settings['scaleFactor']/72.
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

    def displayedWidth(self):
        resol = self.s_settings['resolution']['resolutionX']
        w = (resol/72.0)*self.m_size.width()
        return w

    def displayedHeight(self):
        resol = self.s_settings['resolution']['resolutionY']
        h = (resol/72.0)*self.m_size.height()
        return h

    def setScaleFactor(self, scaleFactor):

        if (self.s_settings['scaleFactor'] != scaleFactor) and scaleFactor > 0.:
            self.refresh()
            self.s_settings['scaleFactor'] = scaleFactor
            self.prepareGeometryChange()
            self.prepareGeometry()

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

    def index(self):
        return self.m_index

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

    def findTextInRect(self, rect):
        return self.m_page.text(rect)

    def search(self, text):
        return self.m_page.search(text)

    def scaleFactor(self):
        return self.s_settings['scaleFactor']

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

        proxyPadding=self.s_settings['pageItem']['proxyPadding']

        x=max([x, self.m_boundingRect.left()+proxyPadding])
        y=max([y, self.m_boundingRect.top()+ proxyPadding])
        width=min([width, self.m_boundingRect.right()-proxyPadding-x])
        height=min([height, self.m_boundingRect.bottom()-y])

        proxy.setGeometry(QRectF(x, y, width, height))

    def scaledResolutionX(self):
        devicePixelRatio = self.s_settings['resolution']['devicePixelRatio']
        resolutionX = self.s_settings['resolution']['resolutionX']
        scaleFactor = self.s_settings['scaleFactor']
        return scaleFactor*devicePixelRatio*resolutionX

    def scaledResolutionY(self):
        devicePixelRatio = self.s_settings['resolution']['devicePixelRatio']
        resolutionY = self.s_settings['resolution']['resolutionY']
        scaleFactor = self.s_settings['scaleFactor']
        return scaleFactor*devicePixelRatio*resolutionY

    def page(self):
        return self.m_page

    def setView(self, view):
        self.m_view=view

    def view(self):
        return self.m_view

    def setHighlightRect(self, rect):
        self.highlightRect=rect

    def highlight(self, painter, optins, widgets):
        if self.highlightRect is None: return
        painter.setBrush(QBrush(QColor(88, 139, 174, 30)))
        painter.drawRect(self.highlightRect)

    def xResolution(self):
        devicePixelRatio = self.s_settings['resolution']['devicePixelRatio']
        resolutionX = self.s_settings['resolution']['resolutionX']
        scaleFactor = self.s_settings['scaleFactor']
        return scaleFactor*devicePixelRatio*resolutionX

    def yResolution(self):
        devicePixelRatio = self.s_settings['resolution']['devicePixelRatio']
        resolutionY = self.s_settings['resolution']['resolutionY']
        scaleFactor = self.s_settings['scaleFactor']
        return scaleFactor*devicePixelRatio*resolutionY

    def clearCursorSelection(self):
        self.m_cursor.clear()

    def getCursorSelection(self):
        return self.m_cursor.get_selection()
