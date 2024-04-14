from gizmo.ui.qt import mixin
from PyQt6 import QtCore, QtGui


class Hint(mixin.view.BaseHint):
    def setup(self):
        self.m_hinting_items = []
        super().setup()

    def connectHint(self):
        for i in self.m_hinting_items:
            i.painted.connect(self.paintHints)

    def disconnectHint(self):
        for i in self.m_hinting_items:
            i.painted.disconnect(self.paintHints)

    def updateHintItems(self):
        for i in self.m_hinting_items:
            i.refresh()

    def cleanUpHinting(self):
        self.updateHintItems()
        self.m_hinting_items = []
        super().cleanUpHinting()

    def createRect(self, d):
        tl = QtCore.QPointF(d[0], d[1])
        br = QtCore.QPointF(d[2], d[3])
        return QtCore.QRectF(tl, br)

    def paintHints(self, painter, opts, widget, item):
        if self.m_hinting:
            hint_painter = self.getHintPainter()
            if hint_painter:
                hint_painter(painter, opts, widget, item)
            else:
                painter.save()
                m = self.m_hint_map.get(item, {})
                painter.setRenderHint(
                        QtGui.QPainter.RenderHint.Antialiasing)
                pen = QtGui.QPen(
                        QtCore.Qt.GlobalColor.black, 0)
                background=QtGui.QColor(128, 128, 255, 128)
                brush=QtGui.QBrush(background)
                for text, data in m.items():
                    box = data["box"]
                    if type(box) == list:
                        box = box[0]
                    rect = item.mapToItem(box, unified=True)
                    top_left = rect.topLeft()
                    painter.fillRect(rect, brush)
                    painter.setPen(pen)
                    painter.drawText(
                            top_left,
                            text)
                painter.restore()

    def setupHint(self, kind, **kwargs):
        vis = self.visibleItems()
        self.m_hinting_items = vis
        super().setupHint(kind, **kwargs)
