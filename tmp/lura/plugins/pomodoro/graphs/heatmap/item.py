from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datetime import *

import matplotlib
import seaborn as sns

class Day(QGraphicsObject):

    mouseDoubleClickEventOccured=pyqtSignal(object)

    def __init__(self, date, db):
        super().__init__()
        self.m_date=date
        self.m_db=db
        self.setup()

    def setup(self):
        self.m_highlight=False
        self.m_plan=10.
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(2, 2, 13, 13)

    def getWorkingHours(self):
        finished=self.m_db.getAll()
        tasks=[]
        for f in finished:
            d=datetime.strptime(f['start'], '%Y-%m-%d %H:%M:%S.%f')
            if d.date()!=self.m_date: continue
            tasks+=[self.m_db.get(f['task_id'])]
        workedHours=0.
        self.perTask={}
        for task in tasks:
            time=0
            duration=task['duration']
            if 'h' in duration:
                hour, duration=tuple(duration.split('h'))
                time+=float(hour)
            if 'm' in duration:
                minute, duration=tuple(duration.split('m'))
                time=float(minute)/60.
            if 's' in duration:
                second=duration.split('s')[0]
                time=float(second)/(60.**2)
            workedHours+=time
            if not task['title'] in self.perTask: self.perTask[task['title']]=0.
            self.perTask[task['title']]+=time
        return workedHours

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickEventOccured.emit(self)

    def hoverMoveEvent(self, event):
        if self.getWorkingHours()<=0.: return
        info='\n'.join([
            'Hours: {}'.format(self.getWorkingHours()),
            'Date: {}'.format(self.m_date)])
        QToolTip.showText(event.screenPos(), info)

    def setHighlight(self, condition):
        self.m_highlight=condition

    def highlight(self):
        return self.m_highlight

    def paint(self, painter, option, widget):

        b=painter.brush()
        p=painter.pen()
        color=QColor(int(self.pos().x()/4), int(self.pos().y()/2), 100)
        if datetime.today().date()==self.m_date: painter.setPen(QColor('#ffff33'))
        if self.highlight():
            painter.setPen(QColor('#ffff88'))
        if datetime.today().date()<self.m_date: 
            color=QColor('#c5c6d0')
        elif self.getWorkingHours()==0.:
            color=QColor('white')
        else:
            cmap=sns.light_palette("seagreen", as_cmap=True)
            value=self.getWorkingHours()/self.m_plan
            color=QColor(matplotlib.colors.to_hex(cmap(value)))

        painter.setBrush(color)
        painter.drawRect(self.boundingRect())
        painter.setBrush(b)
        painter.setPen(p)

        self.setHighlight(False)

    def mousePressEvent(self, event):
        self.setHighlight(True)
        self.update()
