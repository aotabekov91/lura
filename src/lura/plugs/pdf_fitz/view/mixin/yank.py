from gizmo.plug.utils import tag


class Yank:
    canYank = True

    @tag("yy", modes=["normal|^own", "visual[word]|^own"])
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
        self.app.moder.toggle()
        self.cleanUp()
        return text

    @tag("ya", modes=["normal", "visual[word]|^own"])
    def yankToAyleen(self, rstart=1, **kwargs):
        c = self.checkProp("hasServer", self.app)
        if not c:
            return
        sel = self.selection()
        if not sel:
            return
        text = sel.get("text")
        if not text:
            return
        lan = "en"
        if rstart == 2:
            lan = "de"
        req = {
            "target": "Ayleen",
            "object": "app.moder.plugs.deflookup",
            "data": {"term": text, "lan": lan},
            "action": "lookup",
        }
        self.cleanUp()
        return self.app.server.request(**req)
