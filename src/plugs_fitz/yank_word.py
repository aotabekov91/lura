from plug import Plug, tag


class YankWordFitzView:

    canYank = True

    @tag("yy(normal/visual[word])[^]")
    def yankWord(self, *args, **kwargs):
        sel = self.selection()
        if not sel:
            return
        i = sel.get("item")
        e = i.element()
        box = sel.get("box", [])
        text = []
        for i in box:
            r = e.unity(i)
            x, y = r.x(), r.y()
            w, h = x + r.width(), y + r.height()
            r = (x, y, w, h)
            f = e.getBlockText("words", clip=r)
            for i in range(len(f)):
                text += [f[i][4]]
        text = " ".join(text)
        if text:
            c = self.app.qapp.clipboard()
            c.setText(text)
        self.app.stateman.toggle()
        self.cleanUp()
        return text

class FitzYankWord(Plug):

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
        mro=(YankWordFitzView, viewer)
        viewer=type(name, mro, {})
        self.app.buffman.addViewer(name, viewer)
