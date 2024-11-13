from plug import Plug

class FitzYankSelection(Plug):

    def setup(self):
        if self.app.running:
            self.addAGent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAGent)

    def addAGent(self):
        holder=self.app.plugman.plugs.get(
                'YankSelection')
        if holder:
            holder.addAgent('FitzView', self)

    def yank(self, view):
        text=self.yankSelection(view)
        if text:
            clipboard = view.app.qapp.clipboard()
            clipboard.setText(text)
        view.app.stateman.toggle()
        view.cleanUp()
        return text

    def yankSelection(self, view):
        selector=self.app.plugman.plugs.get('Selection')
        selection=selector.selection(view)
        if not selection:
            return
        text = []
        item = selection.get("item")
        element = item.element()
        boxes = selection.get("box", [])
        for box in boxes:
            text+=[self.getBlockText(box, element)]
        return " ".join(text)

    def getBlockText(self, box, element):
        blocker=self.app.plugman.plugs.get(
                'FitzBlockWord')
        if not blocker:
            return ""
        text=[]
        rect = element.unity(box)
        xpos, ypos = rect.x(), rect.y()
        width = xpos + rect.width()
        hight =  ypos + rect.height()
        rect = (xpos, ypos, width, hight)
        block_text = blocker.getBlockText(element, "words", clip=rect)
        for box in range(len(block_text)):
            text += [block_text[box][4]]
        return " ".join(text)
