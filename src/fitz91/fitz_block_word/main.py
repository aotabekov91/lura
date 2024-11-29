from PyQt6 import QtCore

from plug import Plug

class FitzBlockWord(Plug):

    def setup(self):
        super().setup()
        self.m_lasts={}
        self.m_directions={}

    def last(self, element):
        self.m_lasts.get(element)

    def setLast(self, element, last):
        self.m_lasts[element]=last

    def direction(self, element):
        if not element in self.m_directions:
            self.setDirection(element)
        return self.m_directions.get(element)

    def setDirection(self, element, direction=[0, 0]):
        self.m_directions[element]=direction

    def update(self, element, kind=None, selection=None):
        func = getattr(self, kind, None)
        if func:
            func(element, selection)

    def left(self, element, selection):
        direction=self.direction(element)
        if selection and direction[0] == "right":
            self.unRight(element, selection)
        else:
            direction[0]="left"
            self.setDirection(element, direction)
            box, start, end, size = self.getBlockData(element, selection)
            x, y = start.x() - 2, start.y()
            w, h = 5, start.height()
            r = (0, y, x, y + h)
            f = self.getBlockText(element, "words", clip=r)
            if f:
                tl = QtCore.QPointF(f[-1][0], f[-1][1])
                start.setTopLeft(tl)
                box[0] = element.unify(start)
            else:
                r = (0, y - 100, size.width(), y)
                f = self.getBlockText(element, "words", clip=r)
                if f:
                    tl = QtCore.QPointF(f[-1][0], f[-1][1])
                    br = QtCore.QPointF(f[-1][2], f[-1][3])
                    r = QtCore.QRectF(tl, br)
                    box.insert(0, element.unify(r))

    def right(self, element, selection):
        direction=self.direction(element)
        if selection and direction[0] == "left":
            self.unLeft(element, selection)
        else:
            direction[0] = "right"
            self.setDirection(element, direction)
            box, start, end, size = self.getBlockData(
                    element, selection)
            x, y = end.x() + end.width() + 1, end.y()
            w, h = size.width(), end.height()
            r = (x, y, x + w, y + h)
            f = self.getBlockText(element, "words", clip=r)
            if f:
                br = QtCore.QPointF(f[0][2], f[0][3])
                end.setBottomRight(br)
                box[-1] = element.unify(end)
            else:
                r = (0, y + h + 1, x, y + h + 100)
                f = self.getBlockText(element, "words", clip=r)
                if f:
                    tl = QtCore.QPointF(f[0][0], f[0][1])
                    br = QtCore.QPointF(f[0][2], f[0][3])
                    r = QtCore.QRectF(tl, br)
                    box += [element.unify(r)]
            self.updateText(selection)

    def updateText(self, selection):
        text=[]
        boxes=selection['box']
        item=selection['item']
        element=item.element()
        for box in boxes:
            mbox = element.m_norm.mapRect(box)
            x=mbox.x()
            y=mbox.y()
            w=x+mbox.width()
            h=y+mbox.height()
            clip=(x, y, w, h)
            text+=[self.getBlockText(element, 'block', clip=clip)]
        selection['text']= ' '.join(text)

    def toggle(self, element, idx):
        direction=self.direction(element)
        x, y = tuple(direction)
        if idx == 0:
            x = "left" if x == "right" else "right"
        elif idx == 1:
            y = "up" if y == "down" else "down"
        self.setDirection(element, [x, y])

    def changeDirection(self, element):
        direction=self.direction(element)
        x, y = tuple(direction)
        y = "up" if y == "down" else "down"
        x = "left" if x == "right" else "right"
        self.setDirection(element, [x, y])

    def getBlockData(self, element, selection):
        if selection:
            box = selection["box"]
            if len(box) > 0:
                self.setLast(element, selection)
            size = element.size()
            start = element.m_norm.mapRect(box[0])
            end = element.m_norm.mapRect(box[-1])
            return box, start, end, size

    def getBlockText(self, element, *args, **kwargs):
        return element.m_data.get_text(*args, **kwargs)

    def last(self, element, selection):
        direction=self.direction(element)
        direction[0] = "right"
        self.setDirection(element, direction)
        box, start, end, size = self.getBlockData(
                element, selection)
        x, y = end.x(), end.y()
        w, h = element.size().width(), end.height()
        r = (x, y, x + w, y + h)
        f = self.getBlockText(element, "blocks", clip=r)
        if f:
            tl = QtCore.QPointF(f[0][0], f[0][1])
            br = QtCore.QPointF(f[0][2], f[0][3])
            r = QtCore.QRectF(tl, br)
            box[-1] = element.unify(r)

    def first(self, element, selection):
        direction=self.direction(element)
        direction[0] = "left"
        self.setDirection(element, direction)
        b, s, e, size = self.getBlockData(element, selection)
        x, y = 0, s.y()
        w, h = s.x() + s.width(), s.height()
        r = (x, y, x + w, y + h)
        f = self.getBlockText(element, "blocks", clip=r)
        if f:
            tl = QtCore.QPointF(f[0][0], f[0][1])
            br = QtCore.QPointF(f[0][2], f[0][3])
            r = QtCore.QRectF(tl, br)
            b[0] = element.unify(r)

    def down(self, element, selection):
        direction=self.direction(element)
        if selection and direction[1] == "up":
            self.unUp(element, selection)
        else:
            direction[1] = "down"
            self.setDirection(element, direction)
            box, start, end, size = self.getBlockData(
                    element, selection)
            self.update(element, "last", selection)
            x, y = end.x(), end.y() + end.height()
            w, h = end.width(), end.height()
            r = (0, y, x + w, y + h)
            f = self.getBlockText(element, "blocks", clip=r)
            if f:
                tl = QtCore.QPointF(f[0][0], f[0][1])
                br = QtCore.QPointF(f[0][2], f[0][3])
                r = QtCore.QRectF(tl, br)
                box += [element.unify(r)]

    def up(self, element, selection):
        direction=self.direction(element)
        if selection and direction[1] == "down":
            self.unDown(element, selection)
        else:
            direction[1] = "up"
            self.setDirection(element, direction)
            b, s, e, size = self.getBlockData(element, selection)
            self.update(element, "first", selection)
            x, y = s.x(), s.y() - s.height()
            w, h = s.width(), s.height()
            r = (x, y, x + w, y + h)
            f = self.getBlockText(element, "blocks", clip=r)
            if f:
                tl = QtCore.QPointF(f[0][0], f[0][1])
                br = QtCore.QPointF(f[0][2], f[0][3])
                r = QtCore.QRectF(tl, br)
                b.insert(0, element.unify(r))

    def unDown(self, element, selection):
        box, start, end, size = self.getBlockData(element, selection)
        if len(box) > 1:
            selection["box"]=box[:-1]
        else:
            self.changeDirection(element)
            self.up(element, selection)

    def unUp(self, element, selection):
        b, s, e, size = self.getBlockData(element, selection)
        if len(b) > 1:
            selection["box"]=b[1:]
        else:
            self.changeDirection(element)
            self.down(element, selection)

    def unRight(self, element, selection):
        box, start, end, size = self.getBlockData(element, selection)
        x, y = end.x(), end.y()
        w, h = end.width(), end.height()
        r = (x, y, x + w, h + y)
        f = self.getBlockText(element, "words", clip=r)
        if len(f) <= 1:
            self.changeDirection(element)
            self.left(element, selection)
        else:
            br = QtCore.QPointF(f[-2][2], f[-2][3])
            end.setBottomRight(br)
            box[-1] = element.unify(end)

    def unLeft(self, element, selection):
        box, start, end, size = self.getBlockData(element, selection)
        x, y = start.x(), start.y()
        w, h = start.width(), start.height()
        r = (x, y, x + w, h + y)
        f = self.getBlockText(element, "words", clip=r)
        if len(f) <= 1:
            self.changeDirection(element)
            self.right(element, selection)
        else:
            tl = QtCore.QPointF(f[1][0], f[1][1])
            start.setTopLeft(tl)
            box[0] = element.unify(start)

    def jump(self, element, prev_selection, next_selection):
        cb = prev_selection["box"]
        jb = next_selection["box"]
        ctl = cb[0].topLeft()
        cbr = cb[-1].bottomRight()
        jtl = jb[0].topLeft()
        jbr = jb[-1].bottomRight()

        direction=self.direction(element)
        if cbr.y() == jbr.y():
            if cbr.x() < jbr.x():
                direction[0] = "right"
                cb[-1].setBottomRight(jbr)
            else:
                direction[0] = "left"
                cb[-1].setTopLeft(jtl)
        else:
            wf = None
            lines = []
            if cbr.y() > jtl.y():
                self.last(next_selection)
                self.first(prev_selection)
                b, s, e, size = self.getBlockData(next_selection)
                tl = (0, e.bottomRight().y())
                b, s, e, size = self.getBlockData(prev_selection)
                br = (s.topRight().y(), size.width())
                r = (tl[0], tl[1], br[1], br[0])
                wf = self.getBlockText(element, "words", clip=r)
                direction = ["left", "down"]
            elif cbr.y() < jtl.y():
                self.last(prev_selection)
                self.first(next_selection)
                b, s, e, size = self.getBlockData(prev_selection)
                tl = (0, e.bottomRight().y())
                b, s, e, size = self.getBlockData(next_selection)
                br = (s.topRight().y(), size.width())
                r = (tl[0], tl[1], br[1], br[0])
                wf = self.getBlockText(element, "words", clip=r)
                direction = ["right", "down"]
            self.setDirection(element, direction)
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
                i = element.unify(r)
                cb.append(i)
        new_box=sorted(cb, key=lambda r: (r.y(), r.x()))
        prev_selection["box"]=new_box
