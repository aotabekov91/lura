from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datetime import *

from .item import Day

class Heatmap(QGraphicsView):

    widgetDoubleClick=pyqtSignal(object)

    def __init__(self, parent,db=None):
        super().__init__(parent)
        self.m_parent=parent

        self.m_db=db
        self.m_scene=QGraphicsScene(self)
        self.setScene(self.m_scene)
        self.populateScene()
        self.show()

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def populateScene(self):
        today=datetime.today()
        start=datetime(day=1, month=1, year=today.year)
        end=datetime(day=31, month=12, year=today.year)

        column=0
        for date in self.daterange(start, end):

            item=Day(date.date(), self.m_db)
            weekday=date.date().weekday()
            item.setPos(QPoint(column*15, weekday*15))
            self.m_scene.addItem(item)
            item.mouseDoubleClickEventOccured.connect(self.widgetDoubleClick)
            if weekday%6==0 and weekday!=0: column+=1
