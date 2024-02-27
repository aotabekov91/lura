from gizmo.utils import tag
from PyQt5 import QtCore, QtGui


class BoxHint:
    canHintBoxes = True
    hint_box_increment = 0.05

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(self.hintSelectBox)

    @tag("<c-b>", modes=["hint[any]|^"])
    def toggleBoxMode(self, rstart=1):
        sm = self.app.moder.toggleSubmode("box")
        if sm == "box":
            self.m_hint_scale = None
            self.setupHint("box", rstart=rstart)

    @tag("<c-i>", modes=["hint[box]|^"])
    def incrementBoxScale(self, rstart=1):
        self.setupHint("box", rstart=rstart, inc=True)

    @tag("<c-o>", modes=["hint[box]|^"])
    def decrementBoxScale(self, rstart=1):
        self.cleanUpHinting()
        self.setupHint("box", rstart=rstart, inc=False)

    def getBoxHints(self, rstart=1, inc=None):
        alist = []
        if inc is None:
            inc = self.hint_box_increment / rstart
        elif inc and self.m_hint_scale:
            inc = self.m_hint_scale / 2
        elif not inc and self.m_hint_scale:
            inc = self.m_hint_scale * 2
        self.m_hint_scale = inc
        for i in self.visibleItems():
            r = i.boundingRect()
            b = self.getBoxTiles(i, r, inc)
            for d, r in b:
                alist += [{"item": i, "box": [r], "pos": d}]
        return alist

    def getBoxTiles(self, i, r, inc):
        row, col = 0, 0
        e = i.element()
        r = e.unify(r)
        x, y = r.x(), r.y()
        w = x + r.width()
        h = y + r.height()
        hinc = h - y
        while hinc > 0.01:
            col = 0
            x = r.x()
            winc = w - x
            while winc > 0.01:
                pos = (row, col)
                box = QtCore.QRectF(x, y, inc, inc)
                yield (pos, box)
                col += 1
                x += inc
                winc = w - x
            row += 1
            y += inc
            hinc = h - y

    def paintBoxHints(self, p, o, w, i):
        if self.m_hinting:
            p.save()
            f = p.font()
            f.setPointSize(10)
            p.setFont(f)
            m = self.m_hint_map.get(i, {})
            for j, d in m.items():
                b = d["box"][0]
                if d.get("isSelected"):
                    pen = QtGui.QPen(QtCore.Qt.green, 0.0)
                else:
                    pen = QtGui.QPen(QtCore.Qt.yellow, 0.0)
                p.setPen(pen)
                b = i.mapToItem(b, unified=True)
                p.drawRect(b)
                p.drawText(b, QtCore.Qt.AlignCenter, j)
            p.restore()

    def hintSelectBox(self, kind, sel):
        sm = self.app.moder.submode()
        if kind == "box" and sm == "box":
            i = sel["item"]
            self.select(i, sel)
            self.toggleHintMode()
