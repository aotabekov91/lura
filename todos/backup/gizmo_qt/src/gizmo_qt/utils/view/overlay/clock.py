from PyQt6 import QtCore, QtGui, QtWidgets

from gizmo_qt import vimo
from gizmo.utils import tag


class Clock(vimo.View, QtWidgets.QLabel):
    def setup(self):
        super().setup()
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.setupTimer()
        self.hide()

    def setupTimer(self):
        self.m_clock_timer = QtCore.QTimer(self)
        self.m_clock_timer.setInterval(5000)
        self.m_clock_timer.timeout.connect(self.updateClock)
        self.m_clock_timer.start()

    def updateClock(self):
        t = QtCore.QTime.currentTime().toString("hh:mm")
        d = QtCore.QDate.currentDate().toString()
        self.setText(f"{t}\n\n{d}")
        self.setFont(QtGui.QFont("Arial", 30))

    @tag("<c-c>(normal/clock")
    def toggle(self):
        self.updateClock()
        super().toggle()

    def updatePosition(self):
        g = self.parent().geometry()
        self.setGeometry(g)
