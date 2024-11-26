from PyQt6 import QtCore

from plug import Plug


class MouseEvents(Plug, QtCore.QObject):

    def setup(self):
        super().setup()

        # if self.app.running:
        #     self.setFilter()
        # else:
        #     self.app.appSoonStarts.connect(
        #             self.setFilter)

    # def setFilter(self):
        # self.app.view.installEventFilter(self)

    # def eventFilter(self, view, event):
        # print(view, event)
        # return super().eventFilter(view, event)
