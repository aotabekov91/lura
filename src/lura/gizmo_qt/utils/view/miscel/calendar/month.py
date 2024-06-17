from PyQt6 import QtCore, QtWidgets

from lura.qt import vimo

from ...element import ElementView


class CalendarMonthView(
    vimo.View,
    QtWidgets.QWidget,
):
    def setup(self):
        super().setup()
        self.setupUI()

    def setCurrentIndex(self, idx):
        d = idx.day
        y = idx.year
        m = idx.month

    def setupUI(self):
        l = QtWidgets.QGridLayout(self)

        wdays = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]

        for i, t in enumerate(wdays):
            p = (0, i, 1, 1)
            n = "x".join([str(c) for c in p])
            label = QtWidgets.QLabel(t, objectName=t)
            label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )
            label.setFixedSize(40, 40)
            l.addWidget(label, *p)
        for i in range(1, 7):
            p = (i, 0, 1, 1)
            n = "x".join([str(c) for c in p])
            label = QtWidgets.QLabel(
                text=str(i), objectName=n
            )
            label.setFixedSize(20, 20)
            # label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            l.addWidget(label, *p)

        mview = ElementView(
            app=self.app,
            objectName="CalendarMonthView",
        )
        l.addWidget(mview, 1, 1, 6, 7)
        l.setHorizontalSpacing(0)
        l.setVerticalSpacing(0)
        l.setSpacing(0)
        self.mview = mview
