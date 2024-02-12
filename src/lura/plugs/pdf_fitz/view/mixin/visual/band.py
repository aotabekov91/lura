from PyQt5 import QtGui
from PyQt5 import QtCore
from gizmo.utils import tag

class RubberbandVisual:

    canVisualizeRubberband=True

    def setup(self):

        self.m_band_end=None
        self.m_band_start=None
        super().setup()

    @tag('<c-r>', modes=['visual[any]|^own'])
    def toggleVisualBandMode(self):

        if self.checkProp('canHintBoxes'):
            sm=self.app.ui.moder.toggleSubmode('band')
            if sm=='band':
                self.m_band=None
                self.m_band_end=None
                self.m_band_start=None
                self.m_visual_boxes=None
                self.setupHint(
                        kind='visualbox',
                        )
            else:
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
            s=self.m_band.selectionPainted
            s.disconnect(self.paintVisualBand)
        self.m_band=band
        if self.m_band:
            i=self.m_band_start['item']
            s=self.m_band.selectionPainted
            s.connect(self.paintVisualBand)
            self.select(i, band) 

    def paintBandHints(self, p, o, w, i):
        self.paintBoxHints(p, o, w, i)

    def paintVisualBand(self, p, o, w, i):
        pass
