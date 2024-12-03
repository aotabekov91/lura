class Select:
    canSelect = True

    def setup(self):
        super().setup()
        self.m_selection = None
        self.cleanUpWanted.connect(self.cleanUpSelection)
        self.app.earman.delistenWanted.connect(
            self.normalCleanUpSelection
        )

    def normalCleanUpSelection(self):
        m = self.app.stateman.mode()
        if m == "normal":
            self.cleanUpSelection()

    def select(self, i, s, **kwargs):
        if self.checkProp("canSelect", i):
            i.select(s, **kwargs)
            self.m_selection = s

    def selection(self):
        return self.m_selection

    def clearSelection(self):
        for i in self.m_items.values():
            if self.checkProp("canSelect", i):
                i.select()

    def cleanUpSelection(self):
        self.clearSelection()
        self.m_selection = None
