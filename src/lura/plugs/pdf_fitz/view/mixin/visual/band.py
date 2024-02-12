from PyQt5 import QtGui
from PyQt5 import QtCore
from gizmo.utils import tag

class RubberbandVisual:

    rubberbandIncrement=0.05
    canVisualizeRubberband=True

    def setup(self):

        self.m_band=None
        self.m_band_end=None
        self.m_band_start=None
        self.m_band_corner=None
        super().setup()

    @tag('<c-r>', modes=['visual[any]|^own'])
    def toggleVisualBandMode(self):

        if self.checkProp('canHintBoxes'):
            sm=self.app.ui.moder.toggleSubmode('band')
            if sm=='band':
                self.m_band=None
                self.m_band_end=None
                self.m_band_start=None
                self.m_band_corner=None
                self.m_visual_boxes=None
                self.setupHint(
                        kind='visualbox',
                        )
            else:
                self.cleanUpHinting()
                if self.m_band:
                    self.m_band.selectionPainted.disconnect(
                            self.paintVisualBand)

    def updateVisualBandHint(self, key):

        m=self.getHintMatches(key)
        if len(m)==1:
            d=m[list(m.keys())[0]]
            c=d['isSelected']
            d['isSelected']=not c
            self.m_visual_box=d
            self.m_hint_key=''
            self.updateHintItems()
            if not self.m_band_start:
                self.m_band_start=d
            elif not self.m_band_end:
                self.m_band_end=d
                self.m_hint_capturing=False
                self.selectVisualBand()

    def selectVisualBand(self):

        self.cleanUpHinting()
        e=self.m_band_end['box'][0]
        s=self.m_band_start['box'][0]
        s.setBottomRight(e.bottomRight())
        self.setVisualBand(self.m_band_start)

    def setVisualBand(self, band):

        if self.m_band:
            i=self.m_band['item']
            i.selectionPainteddisconnect(
                    self.paintVisualBand)
        self.m_band=band
        self.m_band_corner='topLeft'
        if self.m_band:
            i=self.m_band['item']
            i.selectionPainted.connect(
                    self.paintVisualBand)
            self.select(i, band) 

    @tag('g', modes=['visual[band]|^own'])
    def setBandCorner(self, rstart=None, **kwargs):

        if rstart==1:
            self.m_band_corner='topLeft'
        elif rstart==2:
            self.m_band_corner='topRight'
        elif rstart==3:
            self.m_band_corner='bottomRight'
        else:
            self.m_band_corner='bottomLeft'
        i=self.m_band['item']
        i.refresh()

    @tag('l', modes=['visual[band]|^own'])
    def bandVisualGoToRight(self, rstart=1, **kwargs):

        i=self.m_band['item']
        b=self.m_band['box'][0]
        if self.m_band_corner=='topLeft':
            r=1+self.rubberbandIncrement*rstart
            b.setX(b.x()*r)
        i.refresh()

    @tag('h', modes=['visual[band]|^own'])
    def bandVisualGoToLeft(self, rstart=1, **kwargs):

        i=self.m_band['item']
        b=self.m_band['box'][0]
        if self.m_band_corner=='topLeft':
            r=1-self.rubberbandIncrement*rstart
            b.setX(b.x()*r)
        i.refresh()

    @tag('k', modes=['visual[band]|^own'])
    def bandVisualGoToUp(self, rstart=1, **kwargs):

        i=self.m_band['item']
        b=self.m_band['box'][0]
        if self.m_band_corner=='topLeft':
            r=1-self.rubberbandIncrement*rstart
            b.setY(b.y()*r)
        i.refresh()

    @tag('j', modes=['visual[band]|^own'])
    def bandVisualGoToDown(self, rstart=1, **kwargs):

        i=self.m_band['item']
        b=self.m_band['box'][0]
        if self.m_band_corner=='topLeft':
            r=1+self.rubberbandIncrement*rstart
            b.setY(b.y()*r)
        i.refresh()

    def paintBandHints(self, p, o, w, i):
        self.paintBoxHints(p, o, w, i)

    def paintVisualBand(self, p, o, w, s):

        box=self.m_band['box'][0]
        cf=getattr(box, self.m_band_corner, None)
        if not cf: return
        corner=cf()
        p.save()
        i=s['item']
        c1=i.mapToItem(corner, unified=True)
        if self.m_band_corner=='topLeft':
            c2=QtCore.QPointF(c1.x(), c1.y()+20)
            c3=QtCore.QPointF(c1.x()+20, c1.y())
        elif self.m_band_corner=='topRight':
            c2=QtCore.QPointF(c1.x(), c1.y()+20)
            c3=QtCore.QPointF(c1.x()-20, c1.y())
        elif self.m_band_corner=='bottomRight':
            c2=QtCore.QPointF(c1.x(), c1.y()-20)
            c3=QtCore.QPointF(c1.x()-20, c1.y())
        else:
            c2=QtCore.QPointF(c1.x(), c1.y()-20)
            c3=QtCore.QPointF(c1.x()+20, c1.y())
        pol=QtGui.QPolygonF([c1, c2, c3])
        pen=QtGui.QPen(QtCore.Qt.yellow, 3.0)
        p.setPen(pen)
        p.drawPolygon(pol)
        p.restore()
