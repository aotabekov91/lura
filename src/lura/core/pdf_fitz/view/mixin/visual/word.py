from lura.gizmo.utils import tag


class WordVisual:
    canVisualizeWords = True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(self.jumpToWord)

    def jumpToWord(self, kind, sel):
        if kind == "word":
            m = self.app.stateman.mode()
            sm = self.app.stateman.submode()
            if m == "visual" and sm == "word":
                i = sel["item"]
                e = i.element()
                s = self.selection()
                if s and sel:
                    e.jumpToBlock(s, sel)
                elif sel:
                    i = sel["item"]
                    self.select(i, sel)

    @tag("<escape>/<c-[>(visual[word])[^]")
    def finishVisualWordMode(self):
        self.cleanUpHinting()
        self.cleanUpSelection()
        self.app.stateman.toggle()

    @tag("<c-w>(visual[any])[^]")
    def toggleVisualWordMode(self):
        if self.checkProp("canHintWords"):
            sm = self.app.stateman.toggleSubmode("word")
            if sm == "word" and not self.selection():
                self.setupHint("word")

    @tag("<c-j>(visual[word])[^]")
    def visualWordJumpTo(self):
        self.setupHint("word")

    @tag("o(visual[word])[^]")
    def visualWordGoToFirst(self):
        self.visualWordGoTo(kind="first")

    @tag("$(visual[word])[^]")
    def visualWordGoToEnd(self):
        self.visualWordGoTo(kind="last")

    @tag("k(visual[word])[^]")
    def visualWordGoToUp(self, xrange=[1]):
        self.visualWordGoTo("up", xrange=xrange)

    @tag("j(visual[word])[^]")
    def visualWordGoToDown(self, xrange=[1]):
        self.visualWordGoTo("down", xrange=xrange)

    @tag("l(visual[word])[^]")
    def visualWordGoToLeft(self, xrange=[1]):
        self.visualWordGoTo("right", xrange=xrange)

    @tag("h(visual[word])[^]")
    def visualWordGoToRight(self, xrange=[1]):
        self.visualWordGoTo("left", xrange=xrange)

    @tag("t(visual[word])[^]")
    def toggleWordDirection(self):
        s = self.selection()
        if not s:
            return
        i = s["item"]
        e = i.element()
        e.toggleDirection(0)

    def visualWordGoTo(self, kind, xrange=[1]):
        for i in range(xrange):
            s = self.selection()
            if not s:
                return
            i = s["item"]
            e = i.element()
            e.updateBlock(kind, s)
            i.refresh()
