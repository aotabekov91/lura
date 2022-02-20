from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChartView 

class PieChart(QChartView):

    widgetDoubleClick=pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.m_parent=parent
        self.setup()

    def setup(self):
        self.setRenderHint(QPainter.Antialiasing)

    def on_widgetDoubleClick(self, widget):
        workedHours=widget.getWorkingHours()

        if len(widget.perTask)==0: return

        series=QPieSeries()
        for title, hour in widget.perTask.items():
            series.append(title, hour)

        chart=QChart()
        chart.addSeries(series)
        chart.setTitle('{}: {}'.format(widget.m_date, workedHours))
        chart.legend().hide()

        self.setChart(chart)
        self.show()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.hide()

