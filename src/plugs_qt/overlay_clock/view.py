from PyQt6 import QtCore, QtGui, QtWidgets

from plug_qt import vimo


class ClockView(
        vimo.View, 
        QtWidgets.QLabel
        ):

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

    def toggle(self):
        self.updateClock()
        super().toggle()

    def updatePosition(self):
        parent = self.parent()
        self.setGeometry(parent.geometry())
