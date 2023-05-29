import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .cursor import Cursor
from .pageitem import PageItem
from .layout import DocumentLayout

from lura.utils import Configure, register

class View(QGraphicsView):

    documentModified = pyqtSignal(object)
    continuousModeChanged = pyqtSignal(bool, object)
    currentPageChanged = pyqtSignal(object, int, int)

    scaleModeChanged = pyqtSignal(str, object)
    layoutModeChanged = pyqtSignal(object, object)
    scaleFactorChanged = pyqtSignal([float, object], [int, object])

    keyPressEventOccurred=pyqtSignal(object)
    mouseMoveEventOccured = pyqtSignal(object, object, object)
    hoverMoveEventOccured = pyqtSignal(object, object, object)
    mousePressEventOccured = pyqtSignal(object, object, object)
    mouseDoubleClickOccured = pyqtSignal(object, object, object)
    mouseReleaseEventOccured = pyqtSignal(object, object, object)

    annotationAdded=pyqtSignal(object)
    annotationRemoved=pyqtSignal(object)
    pageHasBeenJustPainted = pyqtSignal(object, object, object, object, object)

    def __init__(self, app, document=None):

        super().__init__(app.main)

        self.app=app

        self.s_cache = {}
        self.m_selection=[]
        self.m_prevPage = 1 
        self.m_currentPage = 1 

        self.m_paintlinks=False

        self.configure=Configure(app, 'View', self)
        self.s_settings=self.configure.getSettings()

        self.cursor=Cursor(self)

        self.m_layout = DocumentLayout(self)
        self.m_thumbnailsScene = QGraphicsScene(self)
        self.m_outlineModel = QStandardItemModel(self)
        self.m_propertiesModel = QStandardItemModel(self)


        self.setup()
        self.connect()

        if document: self.open(document)

    def selection(self): return self.m_selection

    def setSelection(self, selections=[]): self.m_selection=selections

    def setId(self, vid): self.m_id=vid

    def id(self): return self.m_id

    def show(self):

        super().show()
        self.readjust()
        self.fitToPageWidth()
        self.setFocus()

    def connect(self):

        self.annotationAdded.connect(self.app.main.display.annotationAdded)
        self.currentPageChanged.connect(self.app.main.display.currentPageChanged)
        self.mouseDoubleClickOccured.connect(self.app.main.display.mouseDoubleClickOccured)
        self.mouseReleaseEventOccured.connect(self.app.main.display.mouseReleaseEventOccured)
        self.mouseMoveEventOccured.connect(self.app.main.display.mouseMoveEventOccured)
        self.mousePressEventOccured.connect(self.app.main.display.mousePressEventOccured)
        self.hoverMoveEventOccured.connect(self.app.main.display.hoverMoveEventOccured)
        self.pageHasBeenJustPainted.connect(self.app.main.display.pageHasBeenJustPainted)

        self.app.main.display.annotationAdded.connect(self.on_annotationChanged)

    def on_annotationChanged(self, page):

        if self.id()==page.pageItem().view().id(): return
        if page.document().hash()!=self.page().document().hash(): return
        if page.pageNumber()!=self.page().pageNumber(): return
        page.pageItem().refresh(dropCachedPixmap=True)

    def readjust(self):

        left, top=self.saveLeftAndTop()
        self.updateSceneAndView(left, top)

    def setup(self):

        self.proxyWidget=None
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setScene(QGraphicsScene(self))
        self.scene().setBackgroundBrush(QColor('black'))

        self.setAcceptDrops(False)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.verticalScrollBar().valueChanged.connect(self.on_verticalScrollBar_valueChaged)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        try:
            left, top=self.saveLeftAndTop()
            self.updateSceneAndView(left, top)
        except:
            pass
        if not hasattr(self, 'm_pageItems'): return
        for pageItem in self.m_pageItems:
            pageItem.refresh()

    def on_verticalScrollBar_valueChaged(self, int):

        pass

    def jumpToPage(self, page, changeLeft=0., changeTop=0.):

        if page and page >= 0 and page <= len(self.m_pages):
            left, top = self.saveLeftAndTop()
            cond1 = self.m_currentPage != self.m_layout.currentPage(page)
            cond = any([cond1, abs(left-changeLeft) > 0.01])
            cond = any([cond, abs(top-changeTop) > 0.01])
            if cond:
                prevPage=self.m_currentPage
                self.setCurrentPage(self.m_layout.currentPage(page))
                self.prepareView(changeLeft, changeTop, page)

    def saveLeftAndTop(self, left=0., top=0.):

        page=self.m_pageItems[self.m_currentPage-1]
        boundingRect=page.boundingRect().translated(page.pos())
        topLeft=self.mapToScene(self.viewport().rect().topLeft())

        left=(topLeft.x() -boundingRect.x())/boundingRect.width()
        top=(topLeft.y() -boundingRect.y())/boundingRect.height()

        return left, top

    def nextPage(self): self.jumpToPage(self.m_layout.nextPage(self.m_currentPage, len(self.m_pages)))

    def prevPage(self):

        self.jumpToPage(self.m_layout.previousPage(
            self.m_currentPage, len(self.m_pages)))

    def open(self, document):

        self.scene().clear()

        if document is not None:
            
            pages = document.pages().values()

            if len(pages) > 0:
                self.m_pages = pages
                self.m_document = document
                self.preparePages()

            self.refresh()
            self.updateSceneAndView()

            self.setCurrentPage(1)
            self.fitToPageWidth()

            # self.canJumpChanged.emit(False, False)
            # self.continuousModeChanged.emit(self.s_settings['continuousMode'])
            # self.layoutModeChanged.emit(self.m_layout.layoutMode())

            return True

    def refresh(self):

        for pageItem in self.m_pageItems:
            pageItem.refresh(dropCachedPixmap=True)

    def prepareView(self, changeLeft=0., changeTop=0., visiblePage=0):

        rect = self.scene().sceneRect()

        left = rect.left()
        top = rect.top()
        width = rect.width()
        height = rect.height()

        horizontalValue = 0
        verticalValue = 0

        if visiblePage == 0: visiblePage = self.m_currentPage

        for index, page in enumerate(self.m_pageItems):

            boundingRect = page.boundingRect().translated(page.pos())

            if self.s_settings.getboolean('continuousMode', True):
                page.setVisible(True)
            else:
                if self.m_layout.leftIndex(index) == self.m_currentPage-1:
                    page.setVisible(True)
                    top = boundingRect.top() - \
                        self.s_settings.getfloat('pageSpacing', 0.0)
                    height = boundingRect.height()+2. * \
                        self.s_settings.getfloat('pageSpacing', 0,0)
                else:
                    page.setVisible(False)
                    page.cancelRender()

            if index == visiblePage-1:
                horizontalValue = math.floor(
                    boundingRect.left()+changeLeft*boundingRect.width())
                verticalValue = math.floor(
                    boundingRect.top()+changeTop*boundingRect.height())

        #raise highlightIsOnPage

        self.setSceneRect(left, top, width, height)
        self.horizontalScrollBar().setValue(horizontalValue)
        self.verticalScrollBar().setValue(verticalValue)
        self.viewport().update()

    def prepareScene(self, w, h):

        for page in self.m_pageItems:

            page.setResolution(self.logicalDpiX(), self.logicalDpiY())
            dw, dh = page.displayedWidth(), page.displayedHeight()
            fitPageSize=[w/float(dw), h/float(dh)]

            scale = {
                'ScaleFactor': page.scale(),
                'FitToPageWidth': w/dw,
                'FitToPageHeight': min(fitPageSize)
                }

            s=scale[self.s_settings.get('scaleMode', 'FitToPageHeight')]
            page.setScaleFactor(s)

        height = self.s_settings.getfloat('pageSpacing', 0.0)
        left, right, height = self.m_layout.prepareLayout(
            self.m_pageItems, height=height)
        self.scene().setSceneRect(left, 0.0, right-left, height)

    def pageItems(self): return self.m_pageItems

    def pageItem(self, index=None):

        if index is None: index=self.m_currentPage-1
        return self.m_pageItems[index]

    def settings(self): return self.s_settings

    def preparePages(self):

        self.m_pageItems = []

        for i, page in enumerate(self.m_pages):
            pageItem = PageItem(page, self)
            page.setPageItem(pageItem)
            page.annotationAdded.connect(self.app.main.display.annotationAdded)
            self.m_pageItems += [pageItem]

            self.scene().addItem(pageItem)
            # self.pageItemHasBeenJustCreated.emit(pageItem, self)
            pageItem.mouseDoubleClickOccured.connect(self.on_mouseDoubleClickOccured)
            pageItem.mousePressEventOccured.connect(self.on_mousePressEventOccured)
            pageItem.mouseReleaseEventOccured.connect(self.on_mouseReleaseEventOccured)
            pageItem.mouseMoveEventOccured.connect(self.on_mouseMoveEventOccured)
            pageItem.hoverMoveEventOccured.connect(self.on_hoverMoveEventOccured)
            pageItem.pageHasBeenJustPainted.connect(self.on_pageHasBeenJustPainted)

    def on_mouseDoubleClickOccured(self, *args):

        self.mouseDoubleClickOccured.emit(*args, self)

    def on_mousePressEventOccured(self, *args):

        self.mousePressEventOccured.emit(*args, self)

    def on_mouseReleaseEventOccured(self, *args):

        self.mouseReleaseEventOccured.emit(*args, self)

    def on_mouseMoveEventOccured(self, *args):

        self.mouseMoveEventOccured.emit(*args, self)

    def on_hoverMoveEventOccured(self, *args):

        self.hoverMoveEventOccured.emit(*args, self)

    def on_pageHasBeenJustPainted(self, painter, options, widget, page):

        self.pageHasBeenJustPainted.emit(painter, options, widget, page, self)

    def toggleContinuousMode(self):

        self.s_settings['continuousView']=~str(self.s_settings.getboolean('continuousView', False))
        left, top = self.saveLeftAndTop()
        self.adjustScrollBarPolicy()
        self.prepareView(left, top)
        self.continuousModeChanged.emit(self.s_settings.getboolean('continuousView'), self)

    def adjustScrollBarPolicy(self):

        scaleMode = self.s_settings.get('scaleMode', 'FitToPageHeight')
        if scaleMode == 'ScaleFactor':
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageWidth':
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageHeight':
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            policy = Qt.ScrollBarAlwaysOff
            if self.s_settings.getboolean('continuousView', True):
                policy = Qt.ScrollBarAsNeeded

    def incrementDown(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() + visibleHeight
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-0.5))
        else:
            self.verticalScrollBar().setValue(int(self.scene().sceneRect().height()))
        self.setCurrentPageFromVisiblePages()

    def incrementLeft(self):

        self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value()*1.1))

    def incrementRight(self):

        self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value()*0.9))

    def incrementUp(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() - visibleHeight
        if dx>=0:
            self.verticalScrollBar().setValue(int(dx+0.5))
        else:
            self.verticalScrollBar().setValue(0)
        self.setCurrentPageFromVisiblePages()

    def pageUp(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())
        dx=self.verticalScrollBar().value() - visibleHeight
        if dx>=0:
            self.verticalScrollBar().setValue(int(dx+5))
        else:
            self.verticalScrollBar().setValue(0)
        self.setCurrentPageFromVisiblePages()

    def pageDown(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())
        dx=self.verticalScrollBar().value() + visibleHeight
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-5))
        else:
            self.verticalScrollBar().setValue(int(self.scene().sceneRect().height()))
        self.setCurrentPageFromVisiblePages()

    def setCurrentPageFromVisiblePages(self):

        items=self.items(self.viewport().rect())
        if len(items)==1:
            self.setCurrentPage(items[0].page().pageNumber())
        elif len(items)>1:
            visibleHeight=0
            for item in items:
                r=self.viewport().rect()
                viewportRectF=QRectF(r.x(), r.y(), r.width(), r.height())
                intersected=item.boundingRect().intersected(viewportRectF)
                if intersected.height()>visibleHeight:
                    visibleHeight=intersected.height()
                    self.setCurrentPage(item.page().pageNumber())

    def scaleMode(self):

        return self.s_settings.get('scaleMode', 'FitToPageHeight')

    def zoomIn(self): self._zoom(kind='in')

    def zoomOut(self): self._zoom(kind='out')

    def _zoom(self, kind='out'):

        zoomFactor = self.s_settings.getfloat('zoomFactor', .1)
        if self.scaleMode() != 'ScaleFactor': self.setScaleMode('ScaleFactor')

        if kind=='out':
            zoomFactor=1.-zoomFactor
        elif kind=='in':
            zoomFactor=1.+zoomFactor

        left, top = self.saveLeftAndTop()
        for page in self.m_pageItems: page.setScaleFactor(zoomFactor*page.scale())
        self.updateSceneAndView(left=left, top=top)

    def setScaleFactor(self, scaleFactor):

        if self.s_settings.getfloat('scaleFactor', 1.) != scaleFactor:
            if self.scaleMode() == 'ScaleFactor':
                self.s_settings['scaleFactor'] = str(scaleFactor)
                for page in self.m_pageItems:
                    page.setScaleFactor(scaleFactor)
                left, top = self.saveLeftAndTop()
                self.updateSceneAndView(left=left, top=top)

    def fitToPageWidth(self):

        self.setScaleMode('FitToPageWidth')

    def fitToPageHeight(self):

        self.setScaleMode('FitToPageHeight')

    def setScaleMode(self, scaleMode):

        self.s_settings['scaleMode'] = scaleMode
        left, top = self.saveLeftAndTop()
        self.saveLeftAndTop(left, top)
        self.adjustScrollBarPolicy()
        self.updateSceneAndView()
        self.scaleModeChanged.emit(scaleMode, self)

    def lastPage(self): self.jumpToPage(len(self.m_pages))

    def firstPage(self):

        self.jumpToPage(0)

    def activateRubberBand(self, listener=None):

        for page in self.m_pageItems:
            page.activateRubberBand(listener)

    def updateSceneAndView(self, left=0., top=0.):

        visibleWidth=self.m_layout.visibleWidth(self.size().width())
        visibleHeight=self.m_layout.visibleHeight(self.size().height())

        self.prepareScene(visibleWidth, visibleHeight)
        self.prepareView(left, top)

    def save(self, filePath=False, withChanges=True):

        if filePath is False: 
            filePath=self.m_document.filePath()

        tFile=QTemporaryFile()

        if tFile.open(): tFile.close()

        if not self.m_document.save(tFile.fileName(), withChanges=True): return False

        with open(tFile.fileName(), 'rb') as s:

            with open(filePath, 'wb') as d:
                byte = s.read(1024*4)
                while byte != b'':
                    d.write(byte)
                    byte = s.read(1024*4)

        return True
        
    def document(self): return self.m_document

    def currentPage(self): return self.m_currentPage

    def setCurrentPage(self, pageNumber):

        self.m_prevPage=self.m_currentPage
        self.m_currentPage=pageNumber
        if self.m_prevPage!=self.m_currentPage:
            self.currentPageChanged.emit(self.m_document, self.m_currentPage, self.m_prevPage)

    def totalPages(self):

        return len(self.m_pages)

    def paintLinks(self): return self.m_paintlinks

    def setPaintLinks(self, condition=True):

        self.m_paintlinks=condition

        for pageItem in self.m_pageItems:
            pageItem.setPaintLinks(condition)
            pageItem.refresh(dropCachedPixmap=True)

    def update(self, refresh=False):

        pageItem=self.m_pageItems[self.m_currentPage-1]
        pageItem.refresh(dropCachedPixmap=refresh)

    def updateAll(self, refresh=False):

        for pageItem in self.m_pageItems: 
            pageItem.refresh(dropCachedPixmap=refresh)

    def wheelEvent(self, event):

        super().wheelEvent(event)
        self.setCurrentPageFromVisiblePages()

    def event(self, event):

        if event.type()==QEvent.Enter:
            self.setFocus()
            self.app.main.display.setCurrentView(self)
            self.app.modes.setMode('normal')
        return super().event(event)

    def cleanUp(self):

        for pageItem in self.pageItems(): 
            pageItem.setSelection()
            pageItem.setSearched()
