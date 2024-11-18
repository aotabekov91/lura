import typing as tp

from PyQt6 import QtCore, QtWidgets

from plug import utils
from plug_qt.vimo.gizmo import view


class View(
    view.WindowView,
):
    activated: bool = True
    isAppView: bool = True
    windowResized: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def __init__(
        self, app: tp.Any = None, **kwargs
    ) -> None:
        super().__init__(app=app, **kwargs)
        self.setPosIndex(0)

    def setup(self) -> None:
        super().setup()
        self.app.view = self
        self.setupUI()
        self.app.appIsLaunched.connect(
                self.addToBuffer)

    def setupUI(self) -> None:
        tab_klass = utils.Factory(
            view.TileView, QtWidgets.QWidget)
        self.main: view.TabView = view.TabView(
            label="C",
            parent=self,
            app=self.app,
            manager=self,
            name='Center',
            identifier="C",
            tab_classes={"default": tab_klass})
        self.docks: view.Docks = view.Docks(
            label="D",
            parent=self,
            app=self.app,
            manager=self,
            identifier="D")
        self.bar: view.StatusBarView = view.StatusBarView(
            label="S",
            parent=self,
            app=self.app,
            manager=self,
            identifier="S",
            name='Statusbar')
        # self.overlay: view.OverlayView = view.OverlayView(
        #     label="O",
        #     parent=self,
        #     app=self.app,
        #     manager=self,
        #     name='Overlay',
        #     identifier="O")
        self.setContentsMargins(0, 0, 0, 0)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.main)
        self.setStatusBar(self.bar)
        self.main.resized.connect(
                self.resized)

    def addToBuffer(self) -> None:
        self.app.buffman.addView(self.bar)
        self.app.buffman.addView(self.main)
        self.app.buffman.addView(self.docks)
        current = self.main.current
        if current:
            self.app.buffman.addView(current)

    def addView(self, *args, **kwargs):
        self.main.addView(*args, **kwargs)

    def setView(self, *args, **kwargs):
        self.main.setView(*args, **kwargs)
