from gizmo.utils import tag


class WordVisual:
    canVisualizeWords = True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(self.jumpToWord)

    def jumpToWord(self, kind, sel):
        if kind == "word":
            m = self.app.moder.mode()
            sm = self.app.moder.submode()
            if m == "visual" and sm == "word":
                i = sel["item"]
                e = i.element()
                s = self.selection()
                if s and sel:
                    e.jumpToBlock(s, sel)
                elif sel:
                    i = sel["item"]
                    self.select(i, sel)

    @tag(["<escape>", "<c-[>"], modes=["visual[word]|^"])
    def finishVisualWordMode(self):
        self.cleanUpHinting()
        self.cleanUpSelection()
        self.app.moder.toggle()

    @tag("<c-w>", modes=["visual[any]|^"])
    def toggleVisualWordMode(self):
        if self.checkProp("canHintWords"):
            sm = self.app.moder.toggleSubmode("word")
            if sm == "word" and not self.selection():
                self.setupHint("word")

    @tag("<c-j>", modes=["visual[word]|^"])
    def visualWordJumpTo(self):
        self.setupHint("word")

    @tag("o", modes=["visual[word]|^"])
    def visualWordGoToFirst(self):
        self.visualWordGoTo(kind="first")

    @tag("$", modes=["visual[word]|^"])
    def visualWordGoToEnd(self):
        self.visualWordGoTo(kind="last")

    @tag("k", modes=["visual[word]|^"])
    def visualWordGoToUp(self, rstart=1):
        self.visualWordGoTo("up", rstart=rstart)

    @tag("j", modes=["visual[word]|^"])
    def visualWordGoToDown(self, rstart=1):
        self.visualWordGoTo("down", rstart=rstart)

    @tag("l", modes=["visual[word]|^"])
    def visualWordGoToLeft(self, rstart=1):
        self.visualWordGoTo("right", rstart=rstart)

    @tag("h", modes=["visual[word]|^"])
    def visualWordGoToRight(self, rstart=1):
        self.visualWordGoTo("left", rstart=rstart)

    @tag("t", modes=["visual[word]|^"])
    def toggleWordDirection(self):
        s = self.selection()
        if not s:
            return
        i = s["item"]
        e = i.element()
        e.toggleDirection(0)

    def visualWordGoTo(self, kind, rstart=1):
        for i in range(rstart):
            s = self.selection()
            if not s:
                return
            i = s["item"]
            e = i.element()
            e.updateBlock(kind, s)
            i.refresh()
