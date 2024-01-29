from gizmo import mixin
from PyQt5 import QtCore, QtGui

class Hint(mixin.view.Hint):

    def setup(self):

        self.m_hinting_items=[]
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
        self.m_hinting_items=[]
        super().cleanUpHinting()

    def createRect(self, d):

        tl = QtCore.QPointF(d[0], d[1])
        br = QtCore.QPointF(d[2], d[3])
        return QtCore.QRectF(tl, br)

    def paintHints(self, p, o, w, i):

        if self.m_hinting:
            painter=self.getHintPainter()
            if painter:
                painter(p, o, w, i)
            else:
                m=self.m_hint_map.get(i, {})
                p.save()
                pen=QtGui.QPen(QtCore.Qt.red, 0.0)
                p.setPen(pen)
                for j, d in m.items():
                    b=d['box']
                    if type(b)==list: b=b[0]
                    tr=i.mapToItem(b, unified=True)
                    p.drawText(tr.topLeft(), j)
                p.restore()

    def setupHint(self, kind, **kwargs):

        vis=self.visibleItems()
        self.m_hinting_items=vis
        super().setupHint(kind, **kwargs)
