from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Cursor(QObject):

    selectedAreaByCursor=pyqtSignal(object, object, object)

    def __init__(self, parent, settings): 
        super().__init__(parent)
        self.window=parent
        self.s_settings=settings
        self.name='cursor'
        self.height=self.s_settings['height']
        self.tolerance=self.s_settings['tolerance']
        self.cursor=Qt.IBeamCursor
        self.selected=[]
        self.initiate()

    def initiate(self):

        self.m_mode=None
        self.m_rubberBand=None
        self.selectedArea=[]

    def selectWordUnderCursor(self, event, pageItem):

        point=pageItem.mapToPage(event.pos())[0]

        self.point=point
        self.adjustParameters(pageItem)
        width=pageItem.displayedWidth()
        rectF=QRectF(0, self.point.y()-self.height*self.tolerance, width, self.height)

        text=pageItem.findTextInRect(rectF)

        for word in text.split(' '):
            tRectF=pageItem.search(word)

            for i in tRectF:
                if not i.contains(self.point): continue 
                return word, pageItem.mapToPage(i)[1]

    def setup(self, event, pageItem):
        pageItem.setCursor(self.cursor)
        self.displayedWidth=pageItem.displayedWidth()
        self.point=pageItem.mapToPage(event.pos())[0]
        self.adjustParameters(pageItem)

    def adjustParameters(self, pageItem, point=None):
        i=1
        if point is None:
            point=self.point
        while True:
            rectF=QRectF(point.x(), point.y(), i, i)
            text=pageItem.findTextInRect(rectF)
            if text is None:
                i+=1
            else:
                break

        heigt=i

        x=rectF.x()
        y=rectF.y()+heigt*self.tolerance

        point=QPointF(x, y)

        if point is not None:
            return point

        else:
            self.point=point
            self.height=height

    def update(self, point, pageItem):

        startingPosition=self.constructRect(self.point.x(), self.point.y())
        point=self.adjustParameters(pageItem, point)
        newRect=self.constructRect(point.x(), point.y())
        verticalMovement=self.getVerticalMovement(newRect, startingPosition)
        horizontalMovement=self.getHorizontalMovement(newRect, startingPosition)

        if verticalMovement=='sameLine':

            width=abs(newRect.x()-startingPosition.x())
            
            if horizontalMovement=='forwards':

                return [QRectF(startingPosition.x(), startingPosition.y(), width, self.height)]

            elif horizontalMovement=='backwards':

                return [QRectF(newRect.x(), newRect.y(), width, newRect.height())]

        elif verticalMovement=='movingDown':

            firstRowWidth=self.displayedWidth-startingPosition.x()
            firstRow=QRectF(startingPosition.x(), startingPosition.y(),
                    firstRowWidth, self.height)
            lastRow=QRectF(0, newRect.y(), newRect.x(), self.height)

        elif verticalMovement=='movingUp':

            firstRowWidth=self.displayedWidth-newRect.x()
            firstRow=QRectF(newRect.x(), newRect.y(), firstRowWidth, self.height)

            lastRow=QRectF(0, startingPosition.y(), startingPosition.x(), self.height)

        fromAbove=firstRow.y()+firstRow.height()
        fromBelow=lastRow.y()
        inBetween=QRectF(
                0, 
                fromAbove, 
                self.displayedWidth, 
                fromBelow-fromAbove)
        return [firstRow, inBetween, lastRow]


    def getHorizontalMovement(self, newRect, startingPosition):
        difference=newRect.x()-startingPosition.x()
        if difference>0:
            return 'forwards'
        else:
            return 'backwards'

    def getVerticalMovement(self, newRect, startingPosition):
        difference=newRect.y()-startingPosition.y()
        if abs(difference)<self.height*self.tolerance:
            return 'sameLine'
        elif difference>=0.:
            return 'movingDown'
        else:
            return 'movingUp'

    def constructRect(self, x, y):
        return QRectF(x, y, 0, self.height)

    def moveTo(self, event, pageItem):

        pos=pageItem.mapToPage(event.pos())[0]

        rect=self.update(pos, pageItem)

        selected=[]
        selectedText=[]

        if rect is not None:
            for r in rect:
                text=pageItem.findTextInRect(r)
                text=text.split('\n')
                for t in text:
                    tRectF=pageItem.search(t)
                    for i in tRectF:
                        if i.intersects(r):
                            selectedText+=[t]
                            selected+=[pageItem.mapToItem(i)[0]]

        self.selectedText=selectedText
        self.selectedArea=selected
        if len(self.selectedArea)>0:
            pageItem.update()

    def getSelectionArea(self):
        return self.selectedArea

    def getSelectionText(self):
        return self.selectedText

    def setSelectedArea(self, areas):
        self.selectedArea=areas

    def highlightSelectedArea(self, painter, options, widgets):

        if len(self.selectedArea)>0:

            painter.setBrush(QBrush(QColor(88, 139, 174, 30)))
            painter.drawRects(self.selectedArea)

        elif self.m_rubberBand is not None:

            painter.setPen(QPen(Qt.black, 0.0, Qt.DashLine))
            painter.drawRect(self.m_rubberBand)


    def activate(self, client, mode='selector'):
        self.m_client=client
        self.m_mode=mode
        self.connecntSelectorEvents()

    def deactivate(self):
        self.m_client=None
        self.m_mode=None
        self.m_rubberBand=None
        self.unifiedSelection=None
        self.unUnifiedSelection=None
        self.selectedArea=[]
        self.selectedText=[]

    def connecntSelectorEvents(self):
        self.m_client.window.mousePressEventOccured.connect(self.on_mousePress)
        self.m_client.window.mouseMoveEventOccured.connect(self.on_mouseMove)
        self.m_client.window.mouseReleaseEventOccured.connect(self.on_mouseRelease)

    def on_mousePress(self, event, pageItem, view):
        pageItem.pageHasBeenJustPainted.connect(self.highlightSelectedArea)
        if self.m_mode=='selector': 
            self.setup(event, pageItem)
        elif self.m_mode=='rubberBand':
            if event.button()==Qt.LeftButton:
                self.m_rubberBand=QRectF(event.pos(), QSizeF())
                pageItem.update()
                event.accept()

    def on_mouseMove(self, event, pageItem, view):
        if self.m_mode=='selector': 
            self.moveTo(event, pageItem)
        elif self.m_mode=='rubberBand':
            if pageItem.m_boundingRect.contains(event.pos()):
                self.m_rubberBand.setBottomRight(event.pos())
                pageItem.update()
                event.accept()

    def on_mouseRelease(self, event, pageItem, view):
        if self.m_mode is not None:
            try:

                pageItem.pageHasBeenJustPainted.disconnect(self.highlightSelectedArea)
                self.selectedAreaByCursor.emit(event, pageItem, self.m_client)
                self.selectedArea=[]
                pageItem.update()
                event.accept()
            except:
                pass

    def getRubberBandSelection(self):
        return self.m_rubberBand

