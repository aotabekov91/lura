from PyQt6 import QtCore, QtWidgets

from plug_qt import vimo


class CalendarView(
    vimo.View,
    QtWidgets.QWidget,
):
    def setup(self):
        super().setup()
        end = self.m_kwargs.get("end_date", (2970, 1, 1))
        start = self.m_kwargs.get(
            "start_date", (1970, 1, 1)
        )
        self.setMaximumDate(QtCore.QDate(*end))
        self.setMinimumDate(QtCore.QDate(*start))
        self.setMaximumWidth(350)

        # self.setNavigationBarVisible(
        #         False)

        self.setVerticalHeaderFormat(
            QtWidgets.QCalendarWidget.NoVerticalHeader
        )

        # self.setHorizontalHeaderFormat(
        #         QtWidgets.QCalendarWidget.NoHorizontalHeader)
