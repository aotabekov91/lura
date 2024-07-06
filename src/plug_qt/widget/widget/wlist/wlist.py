from PyQt6 import QtCore, QtWidgets


class ListWidget(QtWidgets.QListWidget):
    widgetDataChanged = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )
