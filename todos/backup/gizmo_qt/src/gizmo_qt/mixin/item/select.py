from math import ceil

from PyQt6 import QtCore, QtGui


class Select:
    canSelect = True
    selected = QtCore.pyqtSignal(object)
    selectionPainted = QtCore.pyqtSignal(
        object, object, object, object
    )

    def setup(self):
        self.m_selected = []
        self.select_color = "green"
        self.select_color_alpha = 50
        super().setup()
        self.painted.connect(self.paintSelection)
        self.select_color = QtGui.QColor(self.select_color)
        self.select_color.setAlpha(self.select_color_alpha)
        self.m_select_brush = QtGui.QBrush(
            self.select_color
        )
        self.m_select_pen = QtGui.QPen(self.select_color)

    def selection(self):
        return self.m_selected

    def select(self, s=[], append=False):
        if type(s) != list:
            s = [s]
        if append:
            self.m_selected += s
        else:
            self.m_selected = s
        self.refresh()

    def paintSelection(self, p, o, w, i):
        if self.m_selected:
            p.save()
            for i in self.m_selected:
                box = i.get("box", [])
                rects = []
                for s in box:
                    rects += [
                        self.mapToItem(s, unified=True)
                    ]
                p.setBrush(self.m_select_brush)
                p.drawRects(rects)
                p.setPen(self.m_select_pen)
                p.drawRects(rects)

            p.restore()
            self.selectionPainted.emit(p, o, w, i)
