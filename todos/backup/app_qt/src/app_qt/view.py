import typing as tp

from PyQt6 import QtCore, QtWidgets

from gizmo import utils
from gizmo_qt import mixin
from gizmo_qt.utils import view


class View(
    mixin.view.Exec,
    mixin.view.Hint,
    mixin.view.AppGo,
    mixin.view.Visual,
    mixin.view.Command,
    mixin.view.AppKeyer,
    mixin.view.AppClose,
    mixin.view.ViewHint,
    view.WindowView,
):
    activated: bool = True
    isAppView: bool = True
    cursor_visible: bool = False
    windowResized: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def __init__(
        self, app: tp.Any = None, **kwargs
    ) -> None:
        super().__init__(app=app, **kwargs)
        self.setPosIndex(0)

    def setup(self) -> None:
        super().setup()
        self.app.view = self
        self.setupCursor()
        self.setupUI()
        self.app.appIsLaunched.connect(self.addToUIMan)

    def setupUI(self) -> None:
        self.main: view.TabView = view.TabView(
            label="C",
            parent=self,
            app=self.app,
            manager=self,
            identifier="C",
        )
        self.docks: view.Docks = view.Docks(
            label="D",
            parent=self,
            app=self.app,
            manager=self,
            identifier="D",
        )
        self.bar: view.StatusBarView = view.StatusBarView(
            label="S",
            parent=self,
            app=self.app,
            manager=self,
            identifier="S",
            name='Statusbar',
        )

        # self.overlay: view.OverlayView = view.OverlayView(
        #     label="O",
        #     parent=self,
        #     app=self.app,
        #     manager=self,
        #     name='Overlay',
        #     identifier="O",
        # )

        tab_klass = utils.Factory(
            view.TileView, QtWidgets.QWidget
        )
        self.display: view.TabView = view.TabView(
            label="D",
            app=self.app,
            identifier="D",
            name='Display',
            tab_classes={"default": tab_klass},
        )

        self.setContentsMargins(0, 0, 0, 0)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.display.setContentsMargins(0, 0, 0, 0)

        self.setUtils()
        self.connectUtils()

    def addToUIMan(self) -> None:
        self.app.buffman.addView(self.bar)
        self.app.buffman.addView(self.main)
        self.app.buffman.addView(self.docks)
        self.app.buffman.addView(self.display)
        # self.app.buffman.addView(self.overlay)
        c = self.display.current
        if c:
            self.app.buffman.addView(c)

    def setUtils(self):
        self.main.addView(self.display)
        self.setCentralWidget(self.main)
        self.setStatusBar(self.bar)

    def connectUtils(self):
        self.main.resized.connect(self.resized)
        self.main.resized.connect(self.adjustOverlaySize)

    def addView(self, *args, **kwargs):
        self.main.addView(*args, **kwargs)

    def setView(self, *args, **kwargs):
        self.main.setView(*args, **kwargs)

    @utils.tag("tc(normal)")
    def toggleCursor(self):
        if (
            self.m_cursor
            == QtCore.Qt.CursorShape.BlankCursor
        ):
            self.m_cursor = (
                QtCore.Qt.CursorShape.ArrowCursor
            )
        else:
            self.m_cursor = (
                QtCore.Qt.CursorShape.BlankCursor
            )
        self.setCursor(self.m_cursor)

    def adjustOverlaySize(self, view):
        pass
    #todo
    #     s = self.size()
    #     self.overlay.resize(s)

    def setupCursor(self):
        self.m_cursor = QtCore.Qt.CursorShape.BlankCursor
        self.setCursor(self.m_cursor)
