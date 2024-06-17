from PyQt6 import QtCore


class Connect:
    resized = QtCore.pyqtSignal()
    indexChanged = QtCore.pyqtSignal(object, object)
    positionChanged = QtCore.pyqtSignal(object, object)
    mouseMoveOccured = QtCore.pyqtSignal(object, object)
    hoverMoveOccured = QtCore.pyqtSignal(object, object)
    mousePressOccured = QtCore.pyqtSignal(object, object)
    mouseReleaseOccured = QtCore.pyqtSignal(object, object)
    mouseDoubleClickOccured = QtCore.pyqtSignal(
        object, object
    )
    itemPositionChanged = QtCore.pyqtSignal(
        object, object, object
    )
    itemMouseMoveOccured = QtCore.pyqtSignal(
        object, object, object
    )
    itemHoverMoveOccured = QtCore.pyqtSignal(
        object, object, object
    )
    itemMousePressOccured = QtCore.pyqtSignal(
        object, object, object
    )
    itemMouseReleaseOccured = QtCore.pyqtSignal(
        object, object, object
    )
    itemMouseDoubleClickOccured = QtCore.pyqtSignal(
        object, object, object
    )

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.resized.emit(self, e)

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)
        self.mouseMoveOccured.emit(self, e)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.mousePressOccured.emit(self, e)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.mouseReleaseOccured.emit(self, e)

    def mouseDoubleClickEvent(self, e):
        super().mouseDoubleClickEvent(e)
        self.mouseDoubleClickOccured.emit(self, e)

    def on_itemMouseDoubleClickOccured(self, i, e):
        self.itemMouseDoubleClickOccured.emit(self, i, e)

    def on_itemMousePressOccured(self, i, e):
        self.itemMousePressOccured.emit(self, i, e)

    def on_itemMouseReleaseOccured(self, i, e):
        self.itemMouseReleaseOccured.emit(self, i, e)

    def on_itemMouseMoveOccured(self, i, e):
        self.itemMouseMoveOccured.emit(self, i, e)

    def on_itemHoverMoveOccured(self, i, e):
        self.itemHoverMoveOccured.emit(self, i, e)

    def on_itemPainted(self, p, o, w, i):
        self.itemPainted.emit(self, i, (p, o, w))

    def on_itemAdded(self, item):
        for f in [
            "painted",
            "mouseMoveOccured",
            "hoverMoveOccured",
            "mousePressOccured",
            "mouseReleaseOccured",
            "mouseDoubleClickOccured",
        ]:
            sig = getattr(item, f, None)
            if sig:
                i = f[0].upper() + f[1:]
                n = f"on_item{i}"
                o = getattr(self, n, None)
                if o:
                    sig.connect(o)

    def setup(self):
        super().setup()
        if self.checkProp("hasScene"):
            self.m_scene.itemAdded.connect(
                self.on_itemAdded
            )
        if self.app:
            w = self.app.ui
            self.indexChanged.connect(w.viewIndexChanged)
            self.positionChanged.connect(
                w.viewPositionChanged
            )
            self.mouseDoubleClickOccured.connect(
                w.viewMouseDoubleClickOccured
            )
            self.mouseReleaseOccured.connect(
                w.viewMouseReleaseOccured
            )
            self.mouseMoveOccured.connect(
                w.viewMouseMoveOccured
            )
            self.mousePressOccured.connect(
                w.viewMousePressOccured
            )
            self.hoverMoveOccured.connect(
                w.viewHoverMoveOccured
            )
            self.itemMouseDoubleClickOccured.connect(
                w.viewItemMouseDoubleClickOccured
            )
            self.itemMouseReleaseOccured.connect(
                w.viewItemMouseReleaseOccured
            )
            self.itemMouseMoveOccured.connect(
                w.viewItemMouseMoveOccured
            )
            self.itemMousePressOccured.connect(
                w.viewItemMousePressOccured
            )
            self.itemHoverMoveOccured.connect(
                w.viewItemHoverMoveOccured
            )
