from PyQt6 import QtCore, QtGui


class Block:
    canBlock = True
    direction = [None, None]

    def toggleDirection(self, idx):
        x, y = tuple(self.direction)
        if idx == 0:
            x = "left" if x == "right" else "right"
        elif idx == 1:
            y = "up" if y == "down" else "down"
        self.direction = [x, y]

    def changeDirection(self):
        x, y = tuple(self.direction)
        y = "up" if y == "down" else "down"
        x = "left" if x == "right" else "right"
        self.direction = [x, y]

    def getBlockData(self, sel):
        if sel:
            b = sel["box"]
            if len(b) > 0:
                self.last = sel
            size = self.size()
            s = self.m_norm.mapRect(b[0])
            e = self.m_norm.mapRect(b[-1])
            return b, s, e, size

    def getBlockText(self, *args, **kwargs):
        return self.m_data.get_text(*args, **kwargs)

    def updateBlock(self, kind, sel):
        k = ""
        if kind:
            k = kind[0].title() + kind[1:]
        n = f"block{k}"
        f = getattr(self, n, None)
        if f:
            f(sel)

    def blockLast(self, sel):
        self.direction[0] = "right"
        b, s, e, size = self.getBlockData(sel)
        x, y = e.x(), e.y()
        w, h = self.size().width(), e.height()
        r = (x, y, x + w, y + h)
        f = self.getBlockText("blocks", clip=r)
        if f:
            tl = QtCore.QPointF(f[0][0], f[0][1])
            br = QtCore.QPointF(f[0][2], f[0][3])
            r = QtCore.QRectF(tl, br)
            b[-1] = self.unify(r)

    def blockFirst(self, sel):
        self.direction[0] = "left"
        b, s, e, size = self.getBlockData(sel)
        x, y = 0, s.y()
        w, h = s.x() + s.width(), s.height()
        r = (x, y, x + w, y + h)
        f = self.getBlockText("blocks", clip=r)
        if f:
            tl = QtCore.QPointF(f[0][0], f[0][1])
            br = QtCore.QPointF(f[0][2], f[0][3])
            r = QtCore.QRectF(tl, br)
            b[0] = self.unify(r)

    def blockDown(self, sel):
        if sel and self.direction[1] == "up":
            self.cancelBlockUp(sel)
        else:
            b, s, e, size = self.getBlockData(sel)
            self.updateBlock("last", sel)
            x, y = e.x(), e.y() + e.height() * 1.5
            w, h = e.width(), e.height()
            r = (0, y, x + w, y + h)
            f = self.getBlockText("blocks", clip=r)
            self.direction[1] = "down"
            if f:
                tl = QtCore.QPointF(f[0][0], f[0][1])
                br = QtCore.QPointF(f[0][2], f[0][3])
                r = QtCore.QRectF(tl, br)
                b += [self.unify(r)]

    def blockUp(self, sel):
        if sel and self.direction[1] == "down":
            self.cancelBlockDown(sel)
        else:
            b, s, e, size = self.getBlockData(sel)
            self.updateBlock("first", sel)
            x, y = s.x(), s.y() - s.height() * 1.5
            w, h = s.width(), s.height()
            r = (x, y, x + w, y + h)
            f = self.getBlockText("blocks", clip=r)
            self.direction[1] = "up"
            if f:
                tl = QtCore.QPointF(f[0][0], f[0][1])
                br = QtCore.QPointF(f[0][2], f[0][3])
                r = QtCore.QRectF(tl, br)
                b.insert(0, self.unify(r))

    def blockRight(self, sel):
        if sel and self.direction[0] == "left":
            self.cancelBlockLeft(sel)
        else:
            b, s, e, size = self.getBlockData(sel)
            x, y = e.x() + e.width() + 1, e.y()
            w, h = size.width(), e.height()
            r = (x, y, x + w, y + h)
            f = self.getBlockText("words", clip=r)
            self.direction[0] = "right"
            if f:
                br = QtCore.QPointF(f[0][2], f[0][3])
                e.setBottomRight(br)
                b[-1] = self.unify(e)
            else:
                r = (0, y + h + 1, x, y + h + 100)
                f = self.getBlockText("words", clip=r)
                if f:
                    tl = QtCore.QPointF(f[0][0], f[0][1])
                    br = QtCore.QPointF(f[0][2], f[0][3])
                    r = QtCore.QRectF(tl, br)
                    b += [self.unify(r)]

    def blockLeft(self, sel):
        if sel and self.direction[0] == "right":
            self.cancelBlockRight(sel)
        else:
            self.direction[0] = "left"
            b, s, e, size = self.getBlockData(sel)
            b, s, e, size = self.getBlockData(sel)
            x, y = s.x() - 2, s.y()
            w, h = 5, s.height()
            w, h = size.width(), e.height()
            r = (0, y, x, y + h)
            f = self.getBlockText("words", clip=r)
            if f:
                tl = QtCore.QPointF(f[-1][0], f[-1][1])
                s.setTopLeft(tl)
                b[0] = self.unify(s)
            else:
                r = (0, y - 100, size.width(), y)
                f = self.getBlockText("words", clip=r)
                if f:
                    tl = QtCore.QPointF(f[-1][0], f[-1][1])
                    br = QtCore.QPointF(f[-1][2], f[-1][3])
                    r = QtCore.QRectF(tl, br)
                    b.insert(0, self.unify(r))

    def cancelBlockDown(self, sel):
        b, s, e, size = self.getBlockData(sel)
        if len(b) > 1:
            sel["box"] = b[:-1]
        else:
            self.changeDirection()
            self.blockUp(sel)

    def cancelBlockUp(self, sel):
        b, s, e, size = self.getBlockData(sel)
        if len(b) > 1:
            sel["box"] = b[1:]
        else:
            self.changeDirection()
            self.blockDown(sel)

    def cancelBlockRight(self, sel):
        b, s, e, size = self.getBlockData(sel)
        x, y = e.x(), e.y()
        w, h = e.width(), e.height()
        r = (x, y, x + w, h + y)
        f = self.getBlockText("words", clip=r)
        if len(f) <= 1:
            self.changeDirection()
            self.blockLeft(sel)
        else:
            br = QtCore.QPointF(f[-2][2], f[-2][3])
            e.setBottomRight(br)
            b[-1] = self.unify(e)

    def cancelBlockLeft(self, sel):
        b, s, e, size = self.getBlockData(sel)
        x, y = s.x(), s.y()
        w, h = s.width(), s.height()
        r = (x, y, x + w, h + y)
        f = self.getBlockText("words", clip=r)
        if len(f) <= 1:
            self.changeDirection()
            self.blockRight(sel)
        else:
            tl = QtCore.QPointF(f[1][0], f[1][1])
            s.setTopLeft(tl)
            b[0] = self.unify(s)

    def jumpToBlock(self, csel, jsel):
        cb = csel["box"]
        jb = jsel["box"]
        ctl = cb[0].topLeft()
        cbr = cb[-1].bottomRight()
        jtl = jb[0].topLeft()
        jbr = jb[-1].bottomRight()

        if cbr.y() == jbr.y():
            if cbr.x() < jbr.x():
                self.direction[0] = "right"
                cb[-1].setBottomRight(jbr)
            else:
                self.direction[0] = "left"
                cb[-1].setTopLeft(jtl)
        else:
            wf = None
            lines = []
            if cbr.y() > jtl.y():
                self.blockLast(jsel)
                self.blockFirst(csel)
                b, s, e, size = self.getBlockData(jsel)
                tl = (0, e.bottomRight().y())
                b, s, e, size = self.getBlockData(csel)
                br = (s.topRight().y(), size.width())
                r = (tl[0], tl[1], br[1], br[0])
                wf = self.getBlockText("words", clip=r)
                self.direction = ["left", "down"]
            elif cbr.y() < jtl.y():
                self.blockLast(csel)
                self.blockFirst(jsel)
                b, s, e, size = self.getBlockData(csel)
                tl = (0, e.bottomRight().y())
                b, s, e, size = self.getBlockData(jsel)
                br = (s.topRight().y(), size.width())
                r = (tl[0], tl[1], br[1], br[0])
                wf = self.getBlockText("words", clip=r)
                self.direction = ["right", "down"]
            if wf:
                r = None
                y = None
                for f in wf:
                    br = QtCore.QPointF(f[2], f[3])
                    if f[1] != y:
                        tl = QtCore.QPointF(f[0], f[1])
                        r = QtCore.QRectF(tl, br)
                        lines += [r]
                        y = f[1]
                    else:
                        r.setBottomRight(br)
            for i in jb:
                if i in cb:
                    continue
                cb.append(i)
            for r in lines:
                i = self.unify(r)
                cb.append(i)
        csel["box"] = sorted(cb, key=lambda r: (r.y(), r.x()))
