class State:
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.modelLoaded.connect(self.setStateData)

    def setStateData(self, v, m):
        sm = m.submodel("state")
        if not sm:
            return
        conf = self.m_config.get("State", {})
        for n, c in conf.items():
            if not c:
                continue
            s = m.getState(n, by="state")
            if not s:
                continue
            data = s.data()
            d = {n: data["value"]}
            data.update(d)
            self.setLocator(data, n)
