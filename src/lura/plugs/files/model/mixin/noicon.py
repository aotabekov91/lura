from PyQt5 import QtWidgets, QtGui

class EmptyIconProvider(QtWidgets.QFileIconProvider):

    def icon(self, _):
        return QtGui.QIcon()

class NoIcon:

    def setup(self):

        super().setup()
        self.setIconProvider(EmptyIconProvider())
