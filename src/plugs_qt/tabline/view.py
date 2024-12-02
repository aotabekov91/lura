from PyQt6 import QtCore, QtWidgets


class TablineWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__(objectName="Tabline")
        self.setupUI()
        self.setClock()
        self.updateClock()

    def setupUI(self):
        layout = QtWidgets.QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        layout.setSpacing(0)
        self.andex = QtWidgets.QLabel(
                objectName="AppIndex")
        self.index = QtWidgets.QLabel(
                objectName="TabIndex")
        self.tabs = QtWidgets.QWidget(
                objectName="Tabs")
        tl = QtWidgets.QHBoxLayout(self.tabs)
        self.tabs.setLayout(tl)
        tl.setContentsMargins(0, 0, 0, 0)
        self.clock = QtWidgets.QLabel(
                objectName="Clock")
        self.andex.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.index.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.clock.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.andex)
        layout.addStretch(1)
        layout.addWidget(self.index)
        layout.addStretch(100)
        layout.addWidget(self.tabs)
        layout.addStretch(2)
        layout.addWidget(self.clock)

    def setText(self, kind, text):
        f = getattr(self, kind, None)
        if f:
            f.setText(str(text))
            if text is None:
                return f.hide()
            return f.show()

    def setClock(self):
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start()

    def updateClock(self):
        t = QtCore.QTime.currentTime().toString()
        d = QtCore.QDate.currentDate().toString()
        self.clock.setText(f"{t} {d}")
