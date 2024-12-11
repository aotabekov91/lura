from PyQt6 import QtCore, QtGui

from plug import Plug

class FitzBandVisual(Plug):

    delta = 0.05

    def setup(self):
        super().setup()
        self.m_band = None
        self.m_band_end = None
        self.m_band_start = None
        self.m_band_corner = None
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('BandVisual')
        if holder:
            holder.addAgent('FitzView', self)

    def activate(self, view=None, **kwargs):
        if view:
            self.m_band = None
            self.m_band_end = None
            self.m_band_start = None
            self.m_band_corner = None
            self.m_visual_boxes = None

    def octivate(self, view):
        raise

    def update(self, key):
        m = self.getHintMatches(key)
        if len(m) == 1:
            d = m[list(m.keys())[0]]
            c = d["isSelected"]
            d["isSelected"] = not c
            self.m_visual_box = d
            self.m_hint_key = ""
            self.updateHintItems()
            if not self.m_band_start:
                self.m_band_start = d
            elif not self.m_band_end:
                self.m_band_end = d
                self.m_hint_capturing = False
                self.select()

    def select(self):
        self.cleanUpHinting()
        end = self.m_band_end["box"][0]
        start = self.m_band_start["box"][0]
        start.setBottomRight(end.bottomRight())
        self.setVisualBand(self.m_band_start)

    def setVisualBand(self, band):
        if self.m_band:
            i = self.m_band["item"]
            i.selectionPainteddisconnect(self.paint)
        self.m_band = band
        self.m_band_corner = "topLeft"
        if self.m_band:
            i = self.m_band["item"]
            i.selectionPainted.connect(self.paint)
            self.select(i, band)

    def paintBandHints(self, p, o, w, i):
        self.paintBoxHints(p, o, w, i)

    def paint(self, painter, options, widget, item):
        box = self.m_band["box"][0]
        cf = getattr(box, self.m_band_corner, None)
        if not cf:
            return
        corner = cf()
        painter.save()
        i = item["item"]
        c1 = i.mapToItem(corner, unified=True)
        if self.m_band_corner == "topLeft":
            c2 = QtCore.QPointF(c1.x(), c1.y() + 20)
            c3 = QtCore.QPointF(c1.x() + 20, c1.y())
        elif self.m_band_corner == "topRight":
            c2 = QtCore.QPointF(c1.x(), c1.y() + 20)
            c3 = QtCore.QPointF(c1.x() - 20, c1.y())
        elif self.m_band_corner == "bottomRight":
            c2 = QtCore.QPointF(c1.x(), c1.y() - 20)
            c3 = QtCore.QPointF(c1.x() - 20, c1.y())
        else:
            c2 = QtCore.QPointF(c1.x(), c1.y() - 20)
            c3 = QtCore.QPointF(c1.x() + 20, c1.y())
        pol = QtGui.QPolygonF([c1, c2, c3])
        pen = QtGui.QPen(QtCore.Qt.yellow, 3.0)
        painter.setPen(pen)
        painter.drawPolygon(pol)
        painter.restore()
