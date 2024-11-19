from plug import Plug
from PyQt6 import QtCore, QtGui

class FitzBoxHint(Plug):

    box_increment = 0.05

    def setup(self):
        super().setup()
        self.m_hint=''
        self.m_boxes={}
        self.m_hint_scale = None
        if self.app.running:
            self.addToHinter()
        else:
            self.app.appSoonStarts.connect(
                    self.addToHinter)

    def addToHinter(self):
        hinter=self.app.plugman.getPlug('BoxHint')
        if hinter:
            hinter.addHinter('FitzView', self)

    def boxFunctor(self, key, earman):
        self.m_hint=key
        view=self.app.stateman.view()
        hints=self.m_hints
        if self.m_hint in hints:
            box=hints.get(self.m_hint)
            self.select(view, box)
            box_hinter=self.app.plugman.getPlug(
                    'BoxHint')
            box_hinter.toggle()
            view.redraw()
            return True
        for hint in hints:
            if self.checkHint(hint):
                view.redraw()
                return True
        self.m_hint=''
        view.redraw()
        return False

    def activate(self, view, xrange=[1]):
        self.m_hint_scale=None
        self.assignHints(view)
        view.itemPainted.connect(self.paint)
        self.app.stateman.setFunctor(
                self.boxFunctor)
        view.redraw()

    def octivate(self, view, xrange=[1]):
        self.m_hint=''
        view.itemPainted.disconnect(self.paint)
        self.app.stateman.setFunctor()
        view.redraw()

    def increment(self, view, xrange=[1]):
        self.assignHints(
                view, xrange=xrange, inc=True)
        view.redraw()

    def decrement(self, view, xrange=[1]):
        self.assignHints(
                view, xrange=xrange, inc=False)
        view.redraw()

    def assignHints(self, view, xrange=[1], inc=None):
        all_boxes=[]
        plugs=self.app.plugman.plugs
        hinter=plugs.get('Hint')
        items=view.visibleItems()
        for item in items: 
            boxes=self.getBoxes(
                    item, xrange=xrange, inc=inc)
            self.m_boxes[item]=boxes
            all_boxes+=boxes
        _, hints=hinter.generateHints(all_boxes)
        self.m_hints=hints
        for hint, box in hints.items():
            box['hint']=hint

    def getBoxes(self, item, xrange=[1], inc=None):
        alist = []
        if not xrange:
            xrange=[1]
        if inc is None:
            inc = self.box_increment / xrange[-1]
        elif inc and self.m_hint_scale:
            inc = self.m_hint_scale / 2
        elif not inc and self.m_hint_scale:
            inc = self.m_hint_scale * 2
        self.m_hint_scale = inc
        rect = item.boundingRect()
        element=item.element()
        boxes = self.getTiles(element, rect, inc)
        for pos, box in boxes:
            alist += [{"item": item, "box": [box], "pos": pos}]
        return alist

    def getTiles(self, element, rect, inc):
        row, col = 0, 0
        r = element.unify(rect)
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

    def paint(self, painter, options, widget, item):
        painter.save()
        f = painter.font()
        f.setPointSize(10)
        painter.setFont(f)
        red_pen = QtGui.QPen(QtCore.Qt.GlobalColor.red, 0.0)
        green_pen = QtGui.QPen(QtCore.Qt.GlobalColor.green, 0.0)
        boxes=self.m_boxes.get(item, [])
        for box in boxes:
            hint=box.get("hint")
            box = box.get("box")[0]
            if self.checkHint(hint):
                rect =item.mapToItem(box, unified=True)
                painter.setPen(red_pen)
                painter.drawRect(rect)
                painter.setPen(green_pen)
                painter.drawText(
                        rect, 
                        QtCore.Qt.AlignmentFlag.AlignCenter, 
                        hint)
        painter.restore()

    def select(self, view, data):
        selector=self.app.plugman.getPlug('Selection')
        if selector:
            selector.select(view, **data)

    def checkHint(self, hint):
        partial=hint[:len(self.m_hint)]
        return self.m_hint==partial
