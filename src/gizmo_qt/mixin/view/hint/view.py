from PyQt6 import QtCore, QtWidgets

from app.utils import tag

from .base import BaseHint

class ViewHint(BaseHint):
    canHintViews = True
    view_hint_style = "color: green"
    hintedViewSelected = QtCore.pyqtSignal(object)

    def hintFunctor(self, key, earman):

        digits=earman.digits()
        if digits:
            digits=digits[0]
            super().hintFunctor(digits, earman)
        else:
            self.octivateViewHints()


    def setup(self):
        super().setup()
        self.m_view_hint_labels = {}
        self.hintSelectWanted.connect(self.selectViewHint)
        self.hintFinishWanted.connect(
            self.checkOctivateViewHints
        )

    def checkOctivateViewHints(self):
        if self.m_view_hint_labels:
            self.octivateViewHints()
            self.app.stateman.toggle()

    @tag("<c-v>(hint)")
    def toggleViewHintSubmode(self):
        sm = self.app.stateman.toggleSubmode("view")
        if sm == "view":
            self.activateViewHints()
        else:
            self.octivateViewHints()

    def activateViewHints(self):
        self.m_view_hint_labled = False
        self.painted.connect(self.paintViewHints)
        self.setupHint("view", hint_kind="digit")

    def selectViewHint(self, kind, sel):
        if kind == "view":
            if self.app.stateman.submode() == "view":
                i = sel["view"]
                i.activate()
                self.octivateViewHints()
                self.hintedViewSelected.emit(i)

    def octivateViewHints(self):
        self.m_hinting = False
        labels = self.m_view_hint_labels
        for i, l in labels.items():
            l.hide()
            l.setParent(None)
        self.m_view_hint_labels = {}
        self.painted.disconnect(self.paintViewHints)
        self.update()

    def updateHintItems(self):
        self.update()

    def paintViewHints(self, obj, e):
        if self.m_hinting:
            if self.m_view_hint_labled:
                return
            for n, d in self.m_hint_remap.items():
                l = QtWidgets.QLabel(
                    n,
                    parent=self,
                    objectName="ViewHint",
                )
                b = d["box"]
                l.setGeometry(b)
                w, h = b.width(), b.height()
                l.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )
                s = f"font-size: {min(w, h)}px;"
                self.m_view_hint_labels[n] = l
                s += f"{self.view_hint_style};"
                l.setStyleSheet(s)
                l.show()
            self.m_view_hint_labled = True

    def mapToUI(self, c, ui):
        p = ui.parent()
        if not p:
            return c
        c = ui.mapToParent(c)
        return self.mapToUI(c, p)

    def getViewHints(self, **kwargs):
        alist = []
        views = self.app.buffman.views()
        for v in views:
            if not v.isVisible():
                continue
            if not self.checkProp("canFollow", v):
                continue
            c = QtCore.QPoint(1, 1)
            c = self.mapToUI(c, v)
            r = v.rect()
            x, y = int(c.x() - 1), int(c.y() - 1)
            w, h = r.width(), r.height()
            rect = QtCore.QRect(x, y, w, h)
            alist += [
                {
                    "view": v,
                    "box": rect,
                    "item": self,
                    "pos": (x, y),
                }
            ]
        return sorted(alist, key=lambda d: d["pos"])
