from plug import Plug, tag

class FitzYankWord(Plug):

    def setup(self):
        if self.app.running:
            self.addToYanker()
        else:
            self.app.appSoonStarts.connect(
                    self.addToYanker)

    def addToYanker(self):
        yanker=self.app.plugman.plugs.get(
                'YankWord')
        if yanker:
            yanker.addYanker('FitzView', self)

    def yank(self, view):
        text=self.yankSelectionText(view)
        if text:
            clipboard = view.app.qapp.clipboard()
            clipboard.setText(text)
        view.app.stateman.toggle()
        view.cleanUp()

    def yankSelectionText(self, view):
        selection = view.selection()
        if not selection:
            return
        if 'text' in selection:
            return selection['text']
        text = []
        item = selection.get("item")
        element = item.element()
        boxes = selection.get("box", [])
        for box in boxes:
            text+=[self.getBlockText(box, element)]
        return " ".join(text)

    def getBlockText(self, box, element):
        blocker=self.app.plugman.plugs.get(
                'FitzBlock')
        if not blocker:
            return ""
        text=[]
        rect = element.unity(box)
        xpos, ypos = rect.x(), rect.y()
        width = xpos + rect.width()
        hight =  ypos + rect.height()
        rect = (xpos, ypos, width, hight)
        block_text = element.getBlockText("words", clip=rect)
        for box in range(len(block_text)):
            text += [block_text[box][4]]
        return " ".join(text)
