class UniqLocate:
    def getUniqLocator(
        self,
        data={},
        kind=None,
        **kwargs,
    ):
        f = self.findLocator("getUniq", kind)
        if f:
            return f(data)
        data["hash"] = self.id()
        data["kind"] = self.kind
        return self.createLocator(data)
