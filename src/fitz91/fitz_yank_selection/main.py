from plug import Plug

class FitzYankSelection(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                'normal', None, 'FitzView', 'yankSelection', self.yankSelection)
        self.app.delegman.addAgent(
                'normal', None, 'FitzView', 'yankSelectionToClipboard', self.yankSelection)

    def yankSelectionToClipboard(self, view=None, **kwargs):
        if view:
            text=self.yankSelection(view)
            if text:
                clipboard = view.app.qapp.clipboard()
                clipboard.setText(text)
            # view.app.stateman.activate()
            view.cleanUp()
            return text

    def yankSelection(self, view=None, **kwargs):
        if view:
            selection=self.app.delegman.delegate(
                    action='getSelection', data={'view': view})
            if selection:
                text = []
                item = selection.get("item")
                element = item.element()
                boxes = selection.get("box", [])
                for box in boxes:
                    text+=[self.getBlockText(box, element)]
                view.cleanUp()
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
