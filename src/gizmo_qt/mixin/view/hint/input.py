from PyQt6 import QtCore, QtWidgets

from gizmo.utils import tag

from .base import BaseHint

class InputHint(BaseHint):
    input_hint_style = "color: green"

    def setup(self):
        super().setup()
        self.m_input_hint_labels = {}
        self.hintFinishWanted.connect(
            self.checkOctivateInputHints
        )
        self.hintStarted.connect(self.toggleInputLabels)

    def toggleInputLabels(self):
        sm = self.app.stateman.submode()
        # if sm in ['input|insert', 'input|append']:
        if sm == "input":
            self.paintInputHints()

    def paintInputHints(self):
        if self.m_hinting:
            for n, d in self.m_hint_remap.items():
                l = QtWidgets.QLabel(
                    n,
                    parent=self.app.ui,
                    objectName="InputHint",
                )
                b = d["box"]
                l.setGeometry(b)
                w, h = b.width(), b.height()
                l.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )
                s = f"font-size: {min(w, h)}px;"
                self.m_input_hint_labels[n] = l
                s += f"{self.input_hint_style};"
                l.setStyleSheet(s)
                l.show()

    def checkOctivateInputHints(self):
        if self.m_input_hint_labels:
            self.octivateInputHints()

    @tag("<c-i>(hint)[^]")
    def toggleInputHintSubmode(self):
        if self.checkProp("hasInput"):
            sm = self.app.stateman.toggleSubmode("input")
            if sm != "input":
                self.octivateInputHints()
            else:
                self.activateInputHints()

    @tag("i(hint[input])[^]")
    def enterInputInsertMode(self, xrange=[1]):
        self.octivateInputHints()
        self.toggleInputMode()
        sel, match = self.getMatchedHint(xrange)
        if not sel:
            return
        w = sel.get("view")
        w.setInputMode(True)

    @tag("a(hint[input])[^]")
    def enterInputAppendMode(self, xrange=[1]):
        self.octivateInputHints()
        self.toggleInputMode()
        sel, match = self.getMatchedHint(xrange)
        if not sel:
            return
        w = sel.get("view")
        w.setInputMode(True, mode="append")

    def activateInputHints(self):
        self.m_input_hint_labled = False
        self.setupHint(
            kind="input",
            functor=False,
            hint_kind="xrange",
        )

    def octivateInputHints(self):
        self.m_hinting = False
        labels = self.m_input_hint_labels
        for i, l in labels.items():
            l.hide()
            l.setParent(None)
        self.m_input_hint_labels = {}

    def mapToUI(self, c, ui):
        p = ui.parent()
        if not p:
            return c
        c = ui.mapToParent(c)
        return self.mapToUI(c, p)

    def inputGetWidgets(self):
        widgets = []
        for i in range(self.count()):
            item = self.item(i)
            w = self.itemWidget(item)
            hw = getattr(w, "hasWidgets", None)
            if not hw:
                continue
            for i, p in w.widgets().values():
                cew = getattr(i, "canEdit", False)
                if not cew:
                    continue
                widgets += [i]
        return widgets

    def getInputHints(self, **kwargs):
        alist = []
        self.labels = {}
        wids = self.inputGetWidgets()
        for v in wids:
            if not v.isVisible():
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
