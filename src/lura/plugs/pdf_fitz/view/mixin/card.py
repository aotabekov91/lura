from gizmo.plug.utils import tag


class YankToCard:
    @tag("Cs", modes=["normal|^own"])
    def submitToCard(self, **kwargs):
        if not self.checkProp("hasServer", self.app):
            return
        req = {
            "target": "Anna",
            "action": "submit",
            "object": "app.moder.plugs.card",
        }
        return self.app.server.request(**req)

    @tag("yCa", modes=["normal|^own"])
    def yankAppendToCard(self, rstart=None, **kwargs):
        self.yankToCard(kind="append", rstart=rstart, **kwargs)

    @tag("yCi", modes=["normal|^own"])
    def yankInsertToCard(self, rstart=None, **kwargs):
        self.yankToCard(kind="insert", rstart=rstart, **kwargs)

    @tag("yCs", modes=["normal|^own"])
    def yankSetToCard(self, rstart=None, **kwargs):
        self.yankToCard(kind="set", rstart=rstart, **kwargs)

    def yankToCard(self, kind="set", rstart=None, **kwargs):
        sel = self.selection()
        if not self.checkProp("hasServer", self.app):
            return
        if not sel:
            return
        t = sel.get("text")
        if not t:
            return
        data = {"text": t, "rstart": rstart, "kind": kind}
        req = {
            "data": data,
            "target": "Anna",
            "action": "fetch",
            "object": "app.moder.plugs.card",
        }
        return self.app.server.request(**req)
