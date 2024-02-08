from gizmo.utils import tag

class WordVisual:

    canVisualizeWords=True

    def setup(self):

        super().setup()
        self.hintSelectWanted.connect(
                self.jumpToWord)

    def jumpToWord(self, kind, sel):

        if kind=='word':
            m=self.app.ui.moder.mode()
            sm=self.app.ui.moder.submode()
            if m=='visual' and sm=='word':
                i=sel['item']
                e=i.element()
                s=self.selection()
                if s and sel:
                    e.jumpToBlock(s, sel)
                elif sel:
                    i=sel['item']
                    self.select(i, sel)

    @tag('<c-w>', modes=['visual[any]|^own'])
    def toggleVisualWordMode(self):

        if self.checkProp('canHintWords'):
            sm=self.app.ui.moder.toggleSubmode('word')
            if sm=='word' and not self.selection():
                self.setupHint('word')

    @tag('<c-j>', modes=['visual[word]|^own'])
    def visualWordJumpTo(self):
        self.setupHint('word')

    @tag('o', modes=['visual[word]|^own'])
    def visualWordGoToFirst(self): 
        self.visualWordGoTo(kind='first')

    @tag('$', modes=['visual[word]|^own'])
    def visualWordGoToEnd(self):
        self.visualWordGoTo(kind='last')

    @tag('k', modes=['visual[word]|^own'])
    def visualWordGoToUp(self, rstart=1):
        self.visualWordGoTo('up', rstart=rstart)

    @tag('j', modes=['visual[word]|^own'])
    def visualWordGoToDown(self, rstart=1):
        self.visualWordGoTo('down', rstart=rstart)

    @tag('l', modes=['visual[word]|^own'])
    def visualWordGoToLeft(self, rstart=1):
        self.visualWordGoTo('right', rstart=rstart)

    @tag('h', modes=['visual[word]|^own'])
    def visualWordGoToRight(self, rstart=1):
        self.visualWordGoTo('left', rstart=rstart)

    @tag('t', modes=['visual[word]|^own'])
    def toggleWordDirection(self):

        s=self.selection()
        if not s: return
        i=s['item']
        e=i.element()
        e.toggleDirection(0)

    def visualWordGoTo(self, kind, rstart=1):

        for i in range(rstart):
            s=self.selection()
            if not s: return
            i=s['item']
            e=i.element()
            e.updateBlock(kind, s)
            i.refresh()
