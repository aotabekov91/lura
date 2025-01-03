class Select:
    canSelect = True

    def setup(self):
        super().setup()
        self.m_selection = None
        self.cleanUpWanted.connect(self.clear)
        self.app.earman.delistenWanted.connect(
            self.normalCleanUpSelection
        )

    def normalCleanUpSelection(self):
        m = self.app.stateman.mode()
        if m == "normal":
            self.clear()

    def select(self, i, s, **kwargs):
        if self.checkProp("canSelect", i):
            i.select(s, **kwargs)
            self.m_selection = s

    def selection(self):
        return self.m_selection

    def clear(self):
        for i in self.m_items.values():
            if self.checkProp("canSelect", i):
                i.select()

    def clear(self):
        self.clear()
        self.m_selection = None
