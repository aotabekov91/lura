from PyQt6 import QtCore, QtGui

from lura.qt import vimo, widget
from lura.gizmo.utils import tag


class OverlayInput(
    vimo.View,
    # widget.VimEditor,
):
    blur = False
    textModified = QtCore.pyqtSignal(object)

    def setup(self):
        self.w_ratio = 0.7
        self.h_ratio = 0.7
        self.w_dratio = 0.7
        self.h_dratio = 0.7
        super().setup()
        self.setupUI()
        self.hide()

    @tag("<c-I>(normal/input)[^]")
    def toggle(self, *args, append=True, **kwargs):
        t = kwargs.get("text")
        b = kwargs.get("blur")
        n = kwargs.get("objectName", "OverlayInput")
        if n:
            self.setObjectName(n)
            self.style().unpolish(self)
            self.style().polish(self)
        if not t is None:
            self.setText(t)
        if not b:
            kwargs["blur"] = self.blur
        super().toggle(*args, **kwargs)
        if self.activated:
            self.app.stateman.setMode("input")
        if append:
            c = self.textCursor()
            c.movePosition(
                Qt.CursorShape.ui.QTextCursor.End
            )
            self.setTextCursor(c)

    @tag("<c-m>(input[any])[^]")
    def finishOverlayInputMode(self):
        t = self.text()
        self.octivate()
        self.textModified.emit(t)
        self.app.stateman.toggle()
        self.app.ui.display.activate()

    def setupUI(self):
        self.modeChanged.connect(self.updateInputMode)
        self.app.ui.resized.connect(self.updatePosition)

    def updatePosition(self):
        r = self.parent().rect()
        pw = r.width()
        ph = r.height()
        w = int(pw * self.w_ratio)
        h = int(ph * self.h_ratio)
        x = int(pw / 2 - w / 2)
        y = int(ph / 2 - h / 2)
        self.setGeometry(x, y, w, h)

    def updateInputMode(self, m):
        self.app.stateman.setSubmode(f"NVIM|{m}")
