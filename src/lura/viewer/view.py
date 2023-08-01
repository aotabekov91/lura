import math

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .cursor import Cursor
from .pageitem import PageItem
from .layout import DocumentLayout

from qapp.app import View

class LuraView(View):

    continuousModeChanged = pyqtSignal(bool, object)
    annotationAdded=pyqtSignal(object)
    annotationRemoved=pyqtSignal(object)
    scaleModeChanged = pyqtSignal(object, object)
    scaleFactorChanged = pyqtSignal(object, object)

    def __init__(self, app, layout=DocumentLayout):

        super().__init__(app, layout)

        self.s_cache = {}
        self.m_prevPage = 1 
        self.m_currentPage = 1 
        self.m_paintlinks=False
        self.cursor=Cursor(self)

    def show(self):

        super().show()
        self.readjust()
        self.fitToPageWidth()
        self.setFocus()

    def connect(self):

        super().connect()
        self.annotationAdded.connect(
                self.app.main.display.annotationAdded)
        self.app.main.display.annotationAdded.connect(
                self.on_annotationChanged)
        self.verticalScrollBar().valueChanged.connect(
                self.on_verticalScrollBar_valueChaged)
        self.selection.connect(
                self.app.main.display.viewSelection)

    def on_annotationChanged(self, page):

        if self.id()==page.pageItem().view().id(): return
        if page.model().hash()!=self.page().model().hash(): return
        if page.pageNumber()!=self.page().pageNumber(): return
        page.pageItem().refresh(dropCachedPixmap=True)

    def readjust(self):

        left, top=self.saveLeftAndTop()
        self.updateSceneAndView(left, top)

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

    def on_verticalScrollBar_valueChaged(self, int): pass

    def goto(self, page, changeLeft=0., changeTop=0.):

        if page and page >= 0 and page <= len(self.m_pages):
            left, top = self.saveLeftAndTop()
            cond1 = self.m_currentPage != self.m_layout.currentPage(page)
            cond = any([cond1, abs(left-changeLeft) > 0.01])
            cond = any([cond, abs(top-changeTop) > 0.01])
            if cond:
                self.setCurrentPage(self.m_layout.currentPage(page))
                self.prepareView(changeLeft, changeTop, page)

    def saveLeftAndTop(self, left=0., top=0.):

        page=self.m_pageItems[self.m_currentPage-1]
        boundingRect=page.boundingRect().translated(page.pos())
        topLeft=self.mapToScene(self.viewport().rect().topLeft())

        left=(topLeft.x() -boundingRect.x())/boundingRect.width()
        top=(topLeft.y() -boundingRect.y())/boundingRect.height()

        return left, top

    def next(self): 

        self.goto(self.m_layout.nextPage(
            self.m_currentPage, 
            len(self.m_pages)))

    def prev(self):

        self.goto(self.m_layout.previousPage(
                    self.m_currentPage, 
                    len(self.m_pages)))

    def setModel(self, model):

        super().setModel(model)

        if model:
            pages = model.pages().values()
            if len(pages) > 0:
                self.m_pages = pages
                self.m_model = model
                self.preparePages()

            self.setCurrentPage(0)

            self.refresh()
            self.updateSceneAndView()

            self.setCurrentPage(1)
            self.fitToPageWidth()

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

    def toggleContinuousMode(self):

        # Todo
        return
        cond=str(self.s_settings.getboolean('continuousView', False))
        self.s_settings['continuousView']= not cond
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

    def down(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() + visibleHeight
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-0.5))
        else:
            self.verticalScrollBar().setValue(int(self.scene().sceneRect().height()))
        self.setCurrentPageFromVisiblePages()

    def left(self):

        self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value()*1.1))

    def right(self):

        self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value()*0.9))

    def up(self):

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

    def zoom(self, kind='out'):

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

    def gotoEnd(self): self.goto(len(self.m_pages))

    def gotoBegin(self): self.goto(1)

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
            filePath=self.m_model.filePath()

        tFile=QTemporaryFile()

        if tFile.open(): tFile.close()

        if not self.m_model.save(tFile.fileName(), withChanges=True): return False

        with open(tFile.fileName(), 'rb') as s:

            with open(filePath, 'wb') as d:
                byte = s.read(1024*4)
                while byte != b'':
                    d.write(byte)
                    byte = s.read(1024*4)

        return True
        
    def currentPage(self): return self.m_currentPage

    def setCurrentPage(self, pageNumber):

        self.m_prevPage=self.m_currentPage
        self.m_currentPage=pageNumber
        if self.m_prevPage!=self.m_currentPage:
            item=self.pageItem()
            self.itemChanged.emit(self, item)

    def totalPages(self): return len(self.m_pages)

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
            if pageItem.isVisible():
                pageItem.refresh(dropCachedPixmap=refresh)

    def wheelEvent(self, event):

        super().wheelEvent(event)
        self.setCurrentPageFromVisiblePages()

    def cleanUp(self):

        for pageItem in self.pageItems(): 
            pageItem.select()
            pageItem.setSearched()

    def toggleCursor(self):

        super().toggleCursor()
        for item in self.m_pageItems: item.setCursor(self.m_cursor)

    def name(self):

        if self.m_model:
            return self.m_model.hash()
        else:
            return super().name()
