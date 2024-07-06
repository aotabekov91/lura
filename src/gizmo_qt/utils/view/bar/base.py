from PyQt6 import QtWidgets

from app.utils import tag
from gizmo_qt import vimo, widget


class BaseStatusBarView(
    vimo.View,
    widget.StatusBar,
):
    def setup(self):
        super().setup()
        self.setupContainer()
        self.setupUI()

    def setupUI(self):
        pass

    def setupContainer(self):
        self.container = QtWidgets.QWidget(
            objectName="Container"
        )
        self.container.setContentsMargins(0, 0, 0, 0)
        self.addPermanentWidget(self.container, 10)
        self.m_layout = QtWidgets.QVBoxLayout(
            self.container
        )
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.container.setLayout(self.m_layout)
        self.stack = QtWidgets.QStackedWidget(
            objectName="Stack"
        )
        self.m_layout.addWidget(self.stack)
        self.setContentsMargins(0, 0, 3, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setSizeGripEnabled(False)
        self.layout().setSpacing(0)
        self.stack.hide()
        self.hide()

    @tag("tb(normal)")
    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
