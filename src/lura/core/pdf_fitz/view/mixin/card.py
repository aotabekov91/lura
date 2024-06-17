from lura.gizmo.utils import tag


class YankToCard:
    @tag("Cs(normal)[^]")
    def submitToCard(self, **kwargs):
        if not self.checkProp("hasServer", self.app):
            return
        req = {
            "target": "Anna",
            "action": "submit",
            "object": "app.plugman.plugs.card",
        }
        return self.app.server.request(**req)

    @tag("yCa(normal)[^]")
    def yankAppendToCard(self, xrange=None, **kwargs):
        self.yankToCard(kind="append", xrange=xrange, **kwargs)

    @tag("yCi(normal)[^]")
    def yankInsertToCard(self, xrange=None, **kwargs):
        self.yankToCard(kind="insert", xrange=xrange, **kwargs)

    @tag("yCs(normal)[^]")
    def yankSetToCard(self, xrange=None, **kwargs):
        self.yankToCard(kind="set", xrange=xrange, **kwargs)

    def yankToCard(self, kind="set", xrange=None, **kwargs):
        sel = self.selection()
        if not self.checkProp("hasServer", self.app):
            return
        if not sel:
            return
        t = sel.get("text")
        if not t:
            return
        data = {"text": t, "xrange": xrange, "kind": kind}
        req = {
            "data": data,
            "target": "Anna",
            "action": "fetch",
            "object": "app.plugman.plugs.card",
        }
        return self.app.server.request(**req)
