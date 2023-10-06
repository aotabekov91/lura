import math

from PyQt5 import QtCore
from gizmo.ui import View as BaseView

from .item import Item
from .cursor import Cursor
from .layout import Layout

class View(BaseView):

    annotationAdded=QtCore.pyqtSignal(object)
    annotationRemoved=QtCore.pyqtSignal(object)
    scaleModeChanged = QtCore.pyqtSignal(
            object, object)
    scaleFactorChanged = QtCore.pyqtSignal(
            object, object)
    continuousModeChanged = QtCore.pyqtSignal(
            bool, object)

    def __init__(self, app, layout=Layout):

        super().__init__(app, layout)

        self.s_cache = {}
        self.m_prevPage = 1 
        self.m_currentPage = 1 
        self.m_paintlinks=False
        self.cursor=Cursor(self)
        self.setContentsMargins(0,0,0,0)
        # self.setBackgroundBrush(QtCore.Qt.green)

    def show(self):

        super().show()
        self.readjust()
        self.fitToPageWidth()
        self.setFocus()

    def connect(self):

        super().connect()
        self.annotationAdded.connect(
                self.app.display.annotationAdded)
        self.app.display.annotationAdded.connect(
                self.on_annotationChanged)
        self.verticalScrollBar().valueChanged.connect(
                self.on_verticalScrollBar_valueChaged)
        self.selection.connect(
                self.app.display.viewSelection)

    def on_annotationChanged(self, page):

        if self.id()==page.pageItem().view().id(): return
        if page.model().hash()!=self.page().model().hash(): return
        if page.pageNumber()!=self.page().pageNumber(): return
        page.pageItem().refresh(dropCachedPixmap=True)

    # def readjust(self):
    #     left, top=self.saveLeftAndTop()
    #     self.updateSceneAndView(left, top)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     try:
    #         left, top=self.saveLeftAndTop()
    #         self.updateSceneAndView(left, top)
    #     except:
    #         pass
    #     if not hasattr(self, 'm_pageItems'): return
    #     for pageItem in self.m_pageItems:
    #         pageItem.refresh()

    def on_verticalScrollBar_valueChaged(self, int): 
        pass

    def goto(self, page, changeLeft=0., changeTop=0.):

        if page and page >= 0 and page <= len(self.m_pages):
            left, top = self.saveLeftAndTop()
            c1 = self.m_currentPage != self.m_layout.currentPage(page)
            c = any([c1, abs(left-changeLeft) > 0.001])
            c = any([c, abs(top-changeTop) > 0.001])
            if c:
                self.prepareView(
                        changeLeft, changeTop, page)
                self.setCurrentPageFromVisiblePages()

    def saveLeftAndTop(self, left=0., top=0.):

        page=self.m_pageItems[self.m_currentPage-1]
        rec=page.boundingRect().translated(page.pos())
        topLeft=self.mapToScene(self.viewport().rect().topLeft())
        left=(topLeft.x() -rec.x())/rec.width()
        top=(topLeft.y() -rec.y())/rec.height()
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

            # self.setCurrentPage(0)

            self.refresh()
            self.updateSceneAndView()

            # self.setCurrentPage(1)
            self.fitToPageWidth()

    def refresh(self):

        for pageItem in self.m_pageItems:
            pageItem.refresh(dropCachedPixmap=True)

    def prepareView(
            self, 
            changeLeft=0., 
            changeTop=0., 
            visiblePage=0):

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

            if self.s_settings.get('continuousMode', True):
                page.setVisible(True)
            else:
                if self.m_layout.leftIndex(index) == self.m_currentPage-1:
                    page.setVisible(True)
                    top = boundingRect.top()# -  self.s_settings.get('pageSpacing', 0.0)
                    height = boundingRect.height()# + 2. *  self.s_settings.get('pageSpacing', 0,0)
                else:
                    page.setVisible(False)
                    page.cancelRender()

            if index == visiblePage-1:
                horizontalValue = int(
                    boundingRect.left()+changeLeft*boundingRect.width())
                verticalValue = int(
                    boundingRect.top()+changeTop*boundingRect.height())

        #raise highlightIsOnPage

        self.setSceneRect(left, top, width, height)
        self.horizontalScrollBar().setValue(horizontalValue)
        self.verticalScrollBar().setValue(verticalValue)
        self.viewport().update()

    def reportPosition(self):

        left, top = self.saveLeftAndTop()
        self.positionChanged.emit(
                self, 
                self.pageItem(), 
                left, 
                top)

    def prepareScene(self, w, h):

        for page in self.m_pageItems:

            page.setResolution(
                    self.logicalDpiX(), 
                    self.logicalDpiY())
            dw= page.displayedWidth()
            dh = page.displayedHeight()
            fitPageSize=[w/float(dw), h/float(dh)]

            width_ratio=w/dw
            
            scale = {
                'ScaleFactor': page.scale(),
                'FitToPageWidth': width_ratio,
                'FitToPageHeight': min(fitPageSize)
                }

            s=scale[self.s_settings.get('scaleMode', 'FitToPageHeight')]
            page.setScaleFactor(s)

        height = self.s_settings.get('pageSpacing', 0.0)
        # height=0
        left, right, height = self.m_layout.prepareLayout(
            self.m_pageItems, height=height)
        self.scene().setSceneRect(left, 0.0, right-left, height)

    def pageItems(self): 
        return self.m_pageItems

    def pageItem(self, index=None):

        if index is None: 
            index=self.m_currentPage-1
        return self.m_pageItems[index]

    def settings(self): 
        return self.s_settings

    def preparePages(self):

        self.m_pageItems = []
        for i, page in enumerate(self.m_pages):
            pageItem = Item(page, self)
            page.setPageItem(pageItem)
            page.annotationAdded.connect(
                    self.app.display.annotationAdded)
            self.m_pageItems += [pageItem]
            self.scene().addItem(pageItem)

    def toggleContinuousMode(self):

        # Todo
        return
        cond=str(self.s_settings.get('continuousView', False))
        self.s_settings['continuousView']= not cond
        left, top = self.saveLeftAndTop()
        self.adjustScrollBarPolicy()
        self.prepareView(left, top)
        self.continuousModeChanged.emit(
                self.s_settings.get('continuousView'), self)

    def adjustScrollBarPolicy(self):

        scaleMode = self.s_settings.get(
                'scaleMode', 'FitToPageHeight')
        if scaleMode == 'ScaleFactor':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageWidth':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageHeight':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
            policy = QtCore.Qt.ScrollBarAlwaysOff
            if self.s_settings.get('continuousView', True):
                policy = QtCore.Qt.ScrollBarAsNeeded

    def down(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() + visibleHeight
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-0.5))
        else:
            self.verticalScrollBar().setValue(int(self.scene().sceneRect().height()))
        self.setCurrentPageFromVisiblePages()

    def up(self):

        visibleHeight=self.m_layout.visibleHeight(
                self.size().height())*.05
        dx=self.verticalScrollBar().value() - visibleHeight
        if dx>=0:
            self.verticalScrollBar().setValue(int(dx+0.5))
        else:
            self.verticalScrollBar().setValue(0)
        self.setCurrentPageFromVisiblePages()
        
    def left(self):

        self.horizontalScrollBar().setValue(
                int(self.horizontalScrollBar().value()*1.1))
        self.setCurrentPageFromVisiblePages()

    def right(self):

        self.horizontalScrollBar().setValue(
                int(self.horizontalScrollBar().value()*0.9))
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

        r=self.viewport().rect()
        v=QtCore.QRect(int(r.width()/2)-5, int(r.height()/2-5), 10, 10)
        items=self.items(v)
        if items:
            self.setCurrentPage(items[0].page().pageNumber())
        self.reportPosition()

    def scaleMode(self):

        return self.s_settings.get('scaleMode', 'FitToPageHeight')

    def zoomIn(self, digit=1):

        for i in range(digit):
            self._zoom(kind='in')

    def zoomOut(self, digit=1): 

        for i in range(digit):
            self._zoom(kind='out')

    def _zoom(self, kind='out'):

        zoomFactor = self.s_settings.get('zoomFactor', .1)
        if self.scaleMode() != 'ScaleFactor': 
            self.setScaleMode('ScaleFactor')

        if kind=='out':
            zoomFactor=1.-zoomFactor
        elif kind=='in':
            zoomFactor=1.+zoomFactor

        left, top = self.saveLeftAndTop()
        for page in self.m_pageItems: 
            page.setScaleFactor(zoomFactor*page.scale())
        self.updateSceneAndView(left=left, top=top)

    def setScaleFactor(self, scaleFactor):

        if self.s_settings.get('scaleFactor', 1.) != scaleFactor:
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

    def gotoEnd(self): 
        self.goto(len(self.m_pages))

    def gotoBegin(self): 
        self.goto(1)

    def activateRubberBand(self, listener=None):

        for page in self.m_pageItems:
            page.activateRubberBand(listener)

    def updateSceneAndView(self, left=None, top=None):

        if not left or not top:
            left, top = self.saveLeftAndTop()
        visibleWidth=self.m_layout.visibleWidth(self.size().width())
        visibleHeight=self.m_layout.visibleHeight(self.size().height())

        self.prepareScene(visibleWidth, visibleHeight)
        self.prepareView(left, top)

    def save(self, filePath=False, withChanges=True):

        if filePath is False: 
            filePath=self.m_model.filePath()

        tFile=QtCore.QTemporaryFile()

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
