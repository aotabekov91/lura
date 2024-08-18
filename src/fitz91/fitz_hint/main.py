from PyQt6 import QtCore, QtGui

from plug import Plug

class FitzHint(Plug, QtCore.QObject):

    hintStarted = QtCore.pyqtSignal()
    hintFinished = QtCore.pyqtSignal()
    hintSelectWanted = QtCore.pyqtSignal(object, object)
    hintFinishWanted = QtCore.pyqtSignal()
    hintSelected = QtCore.pyqtSignal(object)

    def setup(self):
        self.m_items = []
        self.cleanUpHinting()
        self.hintSelected.connect(self.selectHint)
        self.hintFinished.connect(self.finishHint)
        super().setup()
        
    def hintFunctor(self, key, earman) -> bool:
        c1 = self.m_hinting
        c2 = self.m_hint_capturing
        if c1 and c2 and key:
            self.m_hint_key = key
            updater = self.getHintUpdater()
            if updater:
                updater(self.m_hint_key)
            else:
                self.updateHint(self.m_hint_key)
            return True
        self.app.stateman.setFunctor()
        return False

    def getHintUpdater(self):
        m = self.app.stateman.mode()
        sm = self.app.stateman.submode()
        mn = m.title()
        sn = sm.title()
        mu = getattr(self, f"update{mn}Hint", None)
        return getattr(self, f"update{mn}{sn}Hint", mu)

    def getHintPainter(self):
        k = self.app.stateman.submode()
        if k:
            n = f"paint{k.title()}Hints"
            return getattr(self, n, None)

    def hint(
        self,
        alist=None,
        kind=None,
        **kwargs,
    ):
        self.m_hinting = True
        self.m_hint_capturing = True
        hinter=self.app.plugman.plugs.get('Hint')
        if alist:
            m, mm = hinter.generateHints(
                    alist, kind, **kwargs)
            self.m_hint_map = m
            self.m_hint_remap = mm
            self.connectHint()
            self.updateHintItems()
            self.hintStarted.emit()
        else:
            self.hintFinished.emit()
            self.cleanUpHinting()

    def getHintMatches(self, key=""):
        match = {}
        for k, l in self.m_hint_remap.items():
            if key == k[: len(key)]:
                match[k] = l
        return match

    def getMatchedHint(self, key):
        key = str(key)
        match = self.getHintMatches(key)
        if len(match) == 0:
            self.hintFinished.emit()
            self.hintFinishWanted.emit()
            self.cleanUpHinting()
            self.disconnectHint()
            return True, match
        elif len(match) == 1:
            d = match[list(match.keys())[0]]
            self.hintSelected.emit(d)
            self.cleanUpHinting()
            self.disconnectHint()
            return d, match
        return False, match

    def updateHint(self, key=""):
        m, match = self.getMatchedHint(key)
        if m is None:
            hints = {}
            for k, d in match.items():
                i = d["item"]
                if not i in hints:
                    hints[i] = {}
                hints[i][k] = d
            self.m_hint_map = hints
            self.m_hint_remap = match
            self.updateHintItems()

    def selectHint(self, sel):
        m = self.app.stateman.submode()
        self.hintSelectWanted.emit(m, sel)

    def finishHint(self):
        self.app.stateman.setSubmode()
        self.app.stateman.setFunctor()
        self.cleanUpHinting()

    def setupHint(self, kind, functor=True, **kwargs):
        vis = self.visibleItems()
        self.m_items = vis
        self.m_hinting = True
        self.m_hint_capturing = True
        self.m_hint_functor = functor
        if functor:
            self.app.stateman.setFunctor(self.hintFunctor)
        self.hint(kind=kind, **kwargs)

    def connectHint(self):
        for item in self.m_items:
            item.painted.connect(self.paint)

    def disconnectHint(self):
        for item in self.m_items:
            item.painted.disconnect(self.paint)

    def updateHintItems(self):
        for item in self.m_items:
            item.refresh()

    def cleanUpHinting(self):
        self.updateHintItems()
        self.m_items = []
        self.m_hint_key = ""
        self.m_hinting = False
        self.m_hint_functor = False
        self.m_hint_capturing = False
        self.m_hint_map = {}
        self.m_hint_remap = {}

    def createRect(self, data):
        top_left = QtCore.QPointF(data[0], data[1])
        bottom_right = QtCore.QPointF(data[2], data[3])
        return QtCore.QRectF(top_left, bottom_right)

    def paint(self, painter, opts, widget, item):
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
