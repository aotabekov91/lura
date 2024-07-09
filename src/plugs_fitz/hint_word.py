from plug import Plug, tag

class FitzWordView:
    canHintWords = True

    def setup(self):
        super().setup()
        if self.app.check('canHint', self):
            self.hintSelectWanted.connect(
                    self.selectWordHint)
    @tag("<c-w>(hint)[^]")
    def toggleWords(self):
        if self.app.check('canHint', self):
            self.toggleHintWordMode()

    @tag("<escape>/<c-[>(hint[word])[^]")
    def finishHintWordMode(self):
        self.cleanUpHinting()
        self.cleanUpSelection()
        self.app.stateman.toggle()

    def toggleHintWordMode(self):
        sm = self.app.stateman.toggleSubmode("word")
        if sm == "word":
            self.setupHint("word")

    def getWordHints(self):
        alist = []
        for item in self.m_hinting_items:
            element = item.element()
            tp = item.element().data().get_textpage()
            for word in tp.extractWORDS():
                rect = self.createRect(word)
                box = element.unify(rect)
                alist.append({
                    "item": item, 
                    "box": [box], 
                    "text": word[4] 
                    })
        return alist

    def selectWordHint(self, kind, sel):
        if kind == "word":
            m = self.app.stateman.mode()
            sm = self.app.stateman.submode()
            if m == "hint" and sm == "word":
                i = sel["item"]
                self.select(i, sel)
                self.app.stateman.toggle()

class FitzWords(Plug):

    def setup(self):
        super().setup()
        self.app.appSoonStarts.connect(
                self.updateFitz)

    def updateFitz(self):
        self.app.wait()
        viewers=self.app.buffman.viewers()
        for name, klass in viewers.items():
            if name=='FitzView':
                self.updateFitzViewer(klass)
                break
        self.app.wait(-1)

    def updateFitzViewer(self, viewer):
        name=viewer.__name__
        mro=(FitzWordView, viewer)
        viewer=type(name, mro, {})
        self.app.buffman.addViewer('FitzView', viewer)
