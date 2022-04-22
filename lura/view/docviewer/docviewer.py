import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from functools import partial

from .pageitem import PageItem
from .layout import DocumentLayout
from .settings import settings
from lura.view.base import View

class DocumentView(QGraphicsView, View):

    continuousModeChanged = pyqtSignal(bool, object)
    documentModified = pyqtSignal(object)
    currentPageChanged = pyqtSignal(object, int)

    layoutModeChanged = pyqtSignal(object, object)
    rubberBandModeChanged = pyqtSignal(str, object)
    scaleFactorChanged = pyqtSignal([float, object], [int, object])
    scaleModeChanged = pyqtSignal(str, object)
    rubberBandReady = pyqtSignal(
        object, 'QRectF', 'QRectF', object, object, object)

    mouseDoubleClickOccured = pyqtSignal(object, object, object)
    mouseReleaseEventOccured = pyqtSignal(object, object, object)
    mouseMoveEventOccured = pyqtSignal(object, object, object)
    mousePressEventOccured = pyqtSignal(object, object, object)
    hoverMoveEventOccured = pyqtSignal(object, object, object)

    pageItemHasBeenJustCreated = pyqtSignal(object, object)
    pageHasBeenJustPainted = pyqtSignal(object, object, object, object,
            object)

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.window=parent
        self.configuration=configuration
        self.m_thumbnailsScene = QGraphicsScene(self)
        self.m_outlineModel = QStandardItemModel(self)
        self.m_propertiesModel = QStandardItemModel(self)
        self.m_highlight = QGraphicsScene()
        self.s_settings = settings
        self.m_currentPage = 1
        self.m_layout = DocumentLayout(self)
        self.s_cache = {}
        self.setup()
        self.connect()

    def connect(self):

        self.continuousModeChanged.connect(self.window.continuousModeChanged)
        self.documentModified.connect(self.window.documentModified)
        self.currentPageChanged.connect(self.window.currentPageChanged)
        self.layoutModeChanged.connect(self.window.layoutModeChanged)
        self.rubberBandModeChanged.connect(self.window.rubberBandModeChanged)
        self.scaleFactorChanged.connect(self.window.scaleFactorChanged)
        self.scaleModeChanged.connect(self.window.scaleModeChanged)
        self.rubberBandReady.connect(self.window.rubberBandReady)
        self.mouseDoubleClickOccured.connect(
            self.window.mouseDoubleClickOccured)
        self.mouseReleaseEventOccured.connect(
            self.window.mouseReleaseEventOccured)
        self.mouseMoveEventOccured.connect(self.window.mouseMoveEventOccured)
        self.mousePressEventOccured.connect(self.window.mousePressEventOccured)
        self.hoverMoveEventOccured.connect(self.window.hoverMoveEventOccured)
        self.pageItemHasBeenJustCreated.connect(
            self.window.pageItemHasBeenJustCreated)
        self.pageHasBeenJustPainted.connect(self.window.pageHasBeenJustPainted)

    def readjust(self):
        left, top=self.saveLeftAndTop()
        self.updateSceneAndView(left, top)

    def setup(self):
        
        self.proxyWidget=None
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setScene(QGraphicsScene(self))
        self.scene().setBackgroundBrush(QColor('black'))

        self.setAcceptDrops(False)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.verticalScrollBar().valueChanged.connect(self.on_verticalScrollBar_valueChaged)

        self.shortcuts={key:func for func, key in
                self.getConfiguration('shortcuts').items()}
        self.setActions()
        self.show()


    def setActions(self):
        self.actions=[]
        for key, value in self.shortcuts.items():
            action=QAction()
            action.setShortcut(QKeySequence(key))
            action.setShortcutContext(Qt.WidgetShortcut)
            func=getattr(self, value)
            action.triggered.connect(func)
            self.addAction(action)
            self.actions+=[action]

    def resizeEvent(self, event):
        try:
            left, top=self.saveLeftAndTop()
            self.updateSceneAndView(left, top)
        except:
            pass
        for pageItem in self.m_pageItems:
            pageItem.refresh()
        super().resizeEvent(event)

    def on_verticalScrollBar_valueChaged(self, int):
        pass

    def jumpToPage(self, page, changeLeft=0., changeTop=0.):
        if page >= 0 and page <= len(self.m_pages):
            left, top = self.saveLeftAndTop()
            cond = self.m_currentPage != self.m_layout.currentPage(page)
            cond = any([cond, abs(left-changeLeft) > 0.01])
            cond = any([cond, abs(top-changeTop) > 0.01])
            if cond:
                self.m_currentPage = self.m_layout.currentPage(page)
                self.prepareView(changeLeft, changeTop, page)
                self.currentPageChanged.emit(self.m_document, self.m_currentPage)

    def saveLeftAndTop(self, left=0., top=0.):
        page=self.m_pageItems[self.m_currentPage-1]
        boundingRect=page.boundingRect().translated(page.pos())
        topLeft=self.mapToScene(self.viewport().rect().topLeft())

        left=(topLeft.x() -boundingRect.x())/boundingRect.width()
        top=(topLeft.y() -boundingRect.y())/boundingRect.height()

        return left, top

    def nextPage(self):
        self.jumpToPage(self.m_layout.nextPage(
            self.m_currentPage, len(self.m_pages)))

    def previousPage(self):
        self.jumpToPage(self.m_layout.previousPage(
            self.m_currentPage, len(self.m_pages)))

    def open(self, document):

        self.scene().clear()

        if document is not None:
            
            pages = document.pages()
            self.prepareDocument(document, pages)
            self.refresh()
            self.updateSceneAndView()

            self.currentPageChanged.emit(self.m_document, self.m_currentPage)

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

            if self.s_settings['continuousMode']:
                page.setVisible(True)
            else:
                if self.m_layout.leftIndex(index) == self.m_currentPage-1:
                    page.setVisible(True)
                    top = boundingRect.top() - \
                        self.s_settings['layout']['pageSpacing']
                    height = boundingRect.height()+2. * \
                        self.s_settings['layout']['pageSpacing']
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

    def prepareScene(self, visibleWidth, visibleHeight):

        # BUG
        # visibleWidth = self.m_layout.visibleWidth(self.viewport().width())
        # visibleHeight = self.m_layout.visibleHeight(self.viewport().height())

        for page in self.m_pageItems:

            page.setResolution(self.logicalDpiX(), self.logicalDpiY())

            displayedWidth = page.displayedWidth()
            displayedHeight = page.displayedHeight()

            fitPageSize=[visibleWidth/float(displayedWidth), visibleHeight/float(displayedHeight)]

            scale = {
                'ScaleFactorMode': self.s_settings['scaleFactor'],
                'FitToPageWidthMode': visibleWidth/displayedWidth,
                'FitToPageSizeMode': min(fitPageSize)
                }

            newScaleFactor=scale[self.s_settings['scaleMode']['currentMode']]
            # newScaleFactor=scale['FitToPageSizeMode']

            page.setScaleFactor(newScaleFactor)

        height = self.s_settings['layout']['pageSpacing']
        left, right, height = self.m_layout.prepareLayout(
            self.m_pageItems, height=height)
        self.scene().setSceneRect(left, 0.0, right-left, height)


    def prepareDocument(self, document, pages):
        if len(pages) > 0:
            self.m_pages = pages
            self.m_document = document
            self.preparePages()

    def pageItem(self, index):
        return self.m_pageItems[index]

    def preparePages(self):

        self.m_pageItems = []

        for i, page in enumerate(self.m_pages):

            pageItem = PageItem(page, i, self.s_settings, self)
            pageItem.setView(self)
            page.setPageItem(pageItem)
            self.scene().addItem(pageItem)
            self.m_pageItems += [pageItem]

            self.pageItemHasBeenJustCreated.emit(pageItem, self)

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
        self.s_settings['continuousMode']=~self.s_settings['continuousMode'] 
        left, top = self.saveLeftAndTop()
        self.adjustScrollBarPolicy()
        self.prepareView(left, top)
        self.continuousModeChanged.emit(
                self.s_settings['continuousMode'], self)

    def adjustScrollBarPolicy(self):
        scaleMode = self.s_settings['scaleMode']['currentMode']
        if scaleMode == 'ScaleFactorMode':
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            # self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        elif scaleMode == 'FitToPageWidthMode':
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageSizeMode':
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            policy = Qt.ScrollBarAlwaysOff
            if self.s_settings['continuousMode']:
                policy = Qt.ScrollBarAsNeeded
            # self.setVerticalScrollBarPolicy(policy)

    def getConfiguration(self, kind='shortcuts'):
        ownConfiguration=self.configuration.get(self.__class__.__name__) 
        if ownConfiguration is not None:
            kind=ownConfiguration.get(kind)
            if kind is None:
                return {}
            return kind

    def pageSmallUp(self):
        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() - visibleHeight
        if dx>=0:
            self.verticalScrollBar().setValue(int(dx+0.5))
        else:
            self.verticalScrollBar().setValue(0)
        self.setCurrentPageFromVisiblePages()

    def pageSmallDown(self):
        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() + visibleHeight
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-0.5))
        else:
            self.verticalScrollBar().setValue(int(self.scene().sceneRect().height()))
        self.setCurrentPageFromVisiblePages()

    def pageLeft(self):
        self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value()*1.1))

    def pageRight(self):
        self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value()*0.9))

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
            self.setCurrentPage(items[0].index()+1)
        elif len(items)>1:
            visibleHeight=0
            for item in items:
                r=self.viewport().rect()
                viewportRectF=QRectF(r.x(), r.y(), r.width(), r.height())
                intersected=item.boundingRect().intersected(viewportRectF)
                if intersected.height()>visibleHeight:
                    visibleHeight=intersected.height()
                    self.setCurrentPage(item.index()+1)

    def scaleMode(self):
        return self.s_settings['scaleMode']['currentMode']

    def zoomIn(self):
        self._zoom(kind='in')

    def zoomOut(self, kind='out'):
        self._zoom(kind='out')

    def _zoom(self, kind='out'):

        zoomFactor = self.s_settings['documentView']['zoomFactor']
        scaleFactor = self.s_settings['scaleFactor']

        if self.scaleMode() != 'ScaleFactorMode':
            self.setScaleMode('ScaleFactorMode')

        if kind=='out':
            self.setScaleFactor(scaleFactor/zoomFactor)
        elif kind=='in':
            self.setScaleFactor(zoomFactor*scaleFactor)


    def setScaleFactor(self, scaleFactor):

        if self.s_settings['scaleFactor'] != scaleFactor:

            if self.scaleMode() == 'ScaleFactorMode':

                for page in self.m_pageItems:

                    page.setScaleFactor(scaleFactor)

                left, top = self.saveLeftAndTop()
                self.updateSceneAndView(left=left, top=top)

    def fitToPageWidth(self):
        self.setScaleMode('FitToPageWidthMode')

    def fitToPageSize(self):
        self.setScaleMode('FitToPageSizeMode')

    def setScaleMode(self, scaleMode):

        if self.s_settings['scaleMode']['currentMode'] != scaleMode:

            self.s_settings['scaleMode']['currentMode'] = scaleMode
            left, top = self.saveLeftAndTop()
            self.saveLeftAndTop(left, top)
            self.adjustScrollBarPolicy()
            self.updateSceneAndView()
            self.scaleModeChanged.emit(scaleMode, self)

    def lastPage(self):
        self.jumpToPage(len(self.m_pages)-1)

    def activateRubberBand(self, listener=None):
        for page in self.m_pageItems:
            page.activateRubberBand(listener)

    def updateSceneAndView(self, left=0., top=0.):

        visibleWidth=self.m_layout.visibleWidth(self.size().width())
        visibleHeight=self.m_layout.visibleHeight(self.size().height())

        self.prepareScene(visibleWidth, visibleHeight)
        self.prepareView(left, top)

    def save(self, filePath=False, withChanges=True):

        if filePath is False: filePath=self.m_document.filePath()

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
        
    def document(self):
        return self.m_document

    def currentPage(self):
        return self.m_currentPage

    def setCurrentPage(self, pageNumber):
        self.m_currentPage=pageNumber
        self.currentPageChanged.emit(self.m_document, self.m_currentPage)

    def totalPages(self):
        return len(self.m_pages)

    def update(self):
        pageItem=self.m_pageItems[self.m_currentPage-1]
        pageItem.refresh(dropCachedPixmap=True)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        self.setCurrentPageFromVisiblePages()

    def event(self, event):
        if event.type()==QEvent.Enter: self.window.setView(self)
        return super().event(event)


class Position:

    def __init__(self, page, left, top):
        self.page = page
        self.left = left
        self.top = top
