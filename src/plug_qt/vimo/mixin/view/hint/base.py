from PyQt6 import QtCore

from plug.utils import tag

class BaseHint:
    canHint: bool = True
    alpha: str = "abcdefghijklmnopqrstuvwxyz"
    hintStarted = QtCore.pyqtSignal()
    hintFinished = QtCore.pyqtSignal()
    hintSelectWanted = QtCore.pyqtSignal(object, object)
    hintFinishWanted = QtCore.pyqtSignal()
    hintSelected = QtCore.pyqtSignal(object)

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

    def setup(self):
        self.cleanUpHinting()
        self.hintSelected.connect(self.selectHint)
        self.hintFinished.connect(self.finishHint)
        super().setup()

    def getHintUpdater(self):
        m = self.app.stateman.mode()
        sm = self.app.stateman.submode()
        mn = m.title()
        sn = sm.title()
        mu = getattr(self, f"update{mn}Hint", None)
        return getattr(self, f"update{mn}{sn}Hint", mu)

    @tag("<escape>(hint[any])[^]")
    def finishHintMode(self):
        self.app.stateman.toggle()

    @tag("<c-f>(normal/hint)")
    def toggleHintMode(self):
        m = self.app.stateman.toggle(
            mode="hint",
            delisten=True,
            passive=["hint"],
        )
        if m != "hint":
            self.cleanUpHinting()

    def getHints(self, kind=None, **kwargs):
        if kind:
            n = f"get{kind.title()}Hints"
            f = getattr(self, n, None)
            if f:
                return f(**kwargs)

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
        if not alist:
            alist = self.getHints(kind, **kwargs)
        if alist:
            m, mm = self.generateHints(alist, **kwargs)
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

    def cleanUpHinting(self):
        self.m_hint_key = ""
        self.m_hinting = False
        self.m_hint_functor = False
        self.m_hint_capturing = False
        self.m_hint_map = {}
        self.m_hint_remap = {}

    def generateHints(
        self, alist, hint_kind="letter", **kwargs
    ):
        ll = len(alist)
        al = len(self.alpha)
        (
            l,
            hmap,
            hints,
        ) = (
            0,
            {},
            {},
        )
        while al**l < ll:
            l += 1
        l = max(l, 1)
        for j, d in enumerate(alist):
            self.saveHintPointers(
                j, d, l, hmap, hints, hint_kind
            )
        return hints, hmap

    def saveHintPointers(
        self, j, d, l, hmap, hints, hint_kind
    ):
        item = d["item"]
        if not item in hints:
            hints[item] = {}
        if hint_kind == "letter":
            m = self.remapHintsToLetters(j, l)
        elif hint_kind == "digit":
            m = self.remapHintsToDigits(j, l)
        hints[item][m] = d
        hmap[m] = d

    def remapHintsToDigits(self, n, l):
        return str(n + 1)

    def remapHintsToLetters(self, n, l):
        c = []
        for _ in range(l):
            c.append(self.alpha[n % len(self.alpha)])
            n = n // len(self.alpha)
        return "".join(reversed(c))

    def selectHint(self, sel):
        m = self.app.stateman.submode()
        self.hintSelectWanted.emit(m, sel)

    def setupHint(self, kind, functor=True, **kwargs):
        self.m_hinting = True
        self.m_hint_capturing = True
        self.m_hint_functor = functor
        if functor:
            self.app.stateman.setFunctor(self.hintFunctor)
        self.hint(kind=kind, **kwargs)

    def finishHint(self):
        self.app.stateman.setSubmode()
        self.app.stateman.setFunctor()
        self.cleanUpHinting()

    def updateHintItems(self):
        pass

    def connectHint(self):
        pass

    def disconnectHint(self):
        pass
