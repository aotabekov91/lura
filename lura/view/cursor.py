from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Cursor(QObject):

    selectedAreaByCursor=pyqtSignal(object, object, object)
    rubberBandSelection=pyqtSignal(object, object, object)

    def __init__(self, page_item): 
        super().__init__(page_item)
        self.page_item=page_item

        self.height=10#self.config['height']
        self.tolerance=0.5#self.config['tolerance']

        self.mode='selector'
        self.selected_area=[]
        self.selected_text=[]
        self.m_rubberBand=None

        self.page_item.mousePressEventOccured.connect(self.on_mousePress)
        self.page_item.mouseMoveEventOccured.connect(self.on_mouseMove)
        self.page_item.mouseReleaseEventOccured.connect(self.on_mouseRelease)
        self.page_item.mouseDoubleClickOccured.connect(self.on_doubleClick)
        self.page_item.pageHasBeenJustPainted.connect(self.paint_selection)

    def on_doubleClick(self, event, pageItem):

        point=pageItem.mapToPage(event.pos())[0]

        self.adjust_paramater(pageItem)
        width=pageItem.displayedWidth()
        rectF=QRectF(0, point.y()-self.height*self.tolerance, width, self.height)

        text=pageItem.findTextInRect(rectF)

        for word in text.split(' '):
            tRectF=pageItem.search(word)

            for i in tRectF:
                if i.contains(point):
                    self.selected_text=[word]
                    self.selected_area=[pageItem.mapToItem(i)[0]]
                    pageItem.update()
                    return

    def adjust_paramater(self, pageItem, point=None):
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

    def update_selection(self, point, pageItem):

        point=self.adjust_paramater(pageItem, point)

        startingPosition=QRectF(self.point.x(), self.point.y(), 0, self.height)
        newRect=QRectF(point.x(), point.y(), 0, self.height)

        verticalMovement=self.move_vertically(newRect, startingPosition)
        horizontalMovement=self.move_horizontally(newRect, startingPosition)

        if verticalMovement=='sameLine':
            width=abs(newRect.x()-startingPosition.x())
            if horizontalMovement=='forwards':
                return [QRectF(startingPosition.x(), startingPosition.y(), width, self.height)]

            elif horizontalMovement=='backwards':
                return [QRectF(newRect.x(), newRect.y(), width, newRect.height())]

        elif verticalMovement=='movingDown':
            firstRowWidth=self.displayed_width-startingPosition.x()
            firstRow=QRectF(startingPosition.x(), startingPosition.y(),
                    firstRowWidth, self.height)
            lastRow=QRectF(0, newRect.y(), newRect.x(), self.height)

        elif verticalMovement=='movingUp':
            firstRowWidth=self.displayed_width-newRect.x()
            firstRow=QRectF(newRect.x(), newRect.y(), firstRowWidth, self.height)
            lastRow=QRectF(0, startingPosition.y(), startingPosition.x(), self.height)

        fromAbove=firstRow.y()+firstRow.height()
        fromBelow=lastRow.y()
        inBetween=QRectF(0, fromAbove, self.displayed_width, fromBelow-fromAbove)
        return [firstRow, inBetween, lastRow]

    def move_horizontally(self, newRect, startingPosition):
        difference=newRect.x()-startingPosition.x()
        if difference>0:
            return 'forwards'
        else:
            return 'backwards'

    def move_vertically(self, newRect, startingPosition):
        difference=newRect.y()-startingPosition.y()
        if abs(difference)<self.height*self.tolerance:
            return 'sameLine'
        elif difference>=0.:
            return 'movingDown'
        else:
            return 'movingUp'

    def update_move(self, event, pageItem):

        pos=pageItem.mapToPage(event.pos())[0]
        rect=self.update_selection(pos, pageItem)

        self.selected_text=[]
        self.selected_area=[]

        if rect is None: return

        for r in rect:
            text=pageItem.findTextInRect(r)
            text=text.split('\n')
            for t in text:
                tRectF=pageItem.search(t)
                for i in tRectF:
                    if i.intersects(r):
                        self.selected_text+=[t]
                        self.selected_area+=[pageItem.mapToItem(i)[0]]

        if len(self.selected_area)>0:
            pageItem.update()

    def paint_selection(self, painter, options, widgets):

        if len(self.selected_area)>0:
            painter.setBrush(QBrush(QColor(88, 139, 174, 30)))
            painter.drawRects(self.selected_area)
        elif self.m_rubberBand:
            painter.fillRect(self.m_rubberBand, QBrush(QColor(128, 128, 255, 128)))

    def on_mousePress(self, event, pageItem):
        self.prev_cursor=pageItem.cursor()
        if self.mode=='selector': 
            pageItem.setCursor(Qt.IBeamCursor)
            self.displayed_width=pageItem.displayedWidth()
            self.point=pageItem.mapToPage(event.pos())[0]
            self.adjust_paramater(pageItem)
        elif self.mode=='rubberBand':
            pageItem.setCursor(Qt.CrossCursor)
            self.m_rubberBand=QRectF(event.pos(), QSizeF())
        event.accept()

    def on_mouseMove(self, event, pageItem):
        if self.mode=='selector': 
            self.update_move(event, pageItem)
        elif self.mode=='rubberBand':
            if pageItem.m_boundingRect.contains(event.pos()):
                self.m_rubberBand.setBottomRight(event.pos())
                self.m_rubberBand=self.m_rubberBand.normalized()
                pageItem.update()
        event.accept()

    def on_mouseRelease(self, event, pageItem):
        pageItem.setCursor(self.prev_cursor)

    def clear(self):
        self.mode='selector'
        self.selected_area=[]
        self.selected_text=[]
        self.m_rubberBand=None
        self.page_item.update()

    def get_selection(self):
        return self.selected_text, self.selected_area
