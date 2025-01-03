from plug import Plug

class FitzYankSelection(Plug):

    def setup(self):
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def activate(self, action=None, view=None, **kwargs):
        func = getattr(self, action, None)
        if view and func:
            return func(view=view, **kwargs)

    def addAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            normal.addAgent('yank', 'FitzView', self)

    def yank(self, view=None, kind=None, **kwargs):
        if view:
            if kind=='selection':
                text=self.yankSelection(view)
                if text:
                    clipboard = view.app.qapp.clipboard()
                    clipboard.setText(text)
                view.app.stateman.activate()
                view.cleanUp()

    def yankSelection(self, view):
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view=view)
        if selection:
            text = []
            item = selection.get("item")
            element = item.element()
            boxes = selection.get("box", [])
            for box in boxes:
                text+=[self.getBlockText(box, element)]
            return " ".join(text)

    def getBlockText(self, box, element):
        block=self.app.plugman.getPlug('FitzBlockWord')
        if block:
            text=[]
            rect = element.unity(box)
            xpos, ypos = rect.x(), rect.y()
            width = xpos + rect.width()
            hight =  ypos + rect.height()
            rect = (xpos, ypos, width, hight)
            block_text = block.getBlockText(
                    element, "words", clip=rect)
            for box in range(len(block_text)):
                text += [block_text[box][4]]
            return " ".join(text)
        return ""
