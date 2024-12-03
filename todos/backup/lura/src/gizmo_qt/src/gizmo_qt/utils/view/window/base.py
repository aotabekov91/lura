from PyQt6 import QtCore, QtWidgets

from gizmo_qt import vimo


class WindowView(vimo.View, QtWidgets.QMainWindow):
    def setup(self):
        super().setup()
        self.container = QtWidgets.QWidget(
            objectName="MainWindowContainer"
        )
        self.m_layout = QtWidgets.QVBoxLayout()
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.container.setLayout(self.m_layout)
        self.setCentralWidget(self.container)
        self.setAcceptDrops(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )
