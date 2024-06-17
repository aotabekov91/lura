from lura.gizmo.utils import tag


class WordHint:
    canHintWords = True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(
                self.selectWordHint)

    @tag("<escape>/<c-[>(hint[word])[^]")
    def finishHintWordMode(self):
        self.cleanUpHinting()
        self.cleanUpSelection()
        self.app.stateman.toggle()

    @tag("<c-w>(hint)[^]")
    def toggleHintWordMode(self):
        sm = self.app.stateman.toggleSubmode("word")
        if sm == "word":
            self.setupHint("word")

    def getWordHints(self):
        alist = []
        for i in self.m_hinting_items:
            tl = []
            e = i.element()
            tp = i.element().data().get_textpage()
            for t in tp.extractWORDS():
                r = self.createRect(t)
                r = e.unify(r)
                tl += [{"item": i, "box": [r], "text": t[4]}]
            alist += tl
        return alist

    def selectWordHint(self, kind, sel):
        if kind == "word":
            m = self.app.stateman.mode()
            sm = self.app.stateman.submode()
            if m == "hint" and sm == "word":
                i = sel["item"]
                self.select(i, sel)
                self.app.stateman.toggle()
