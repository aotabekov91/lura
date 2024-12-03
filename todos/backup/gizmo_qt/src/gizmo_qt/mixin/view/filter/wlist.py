class ListWidgetFilter:
    canFilter = True

    def setup(self):
        super().setup()
        self.m_filter_cond = None

    def clearFilter(self):
        self.m_filter_cond = None
        for j in range(self.count()):
            i = self.item(j)
            i.setHidden(False)

    def checkFilter(self, e):
        return True

    def setFilter(self, cond=None):
        if not cond:
            self.clearFilter()
        else:
            self.m_filter_cond = cond
            for j in range(self.count()):
                i = self.item(j)
                e = i.element()
                if self.checkFilter(e):
                    i.setHidden(False)
                else:
                    i.setHidden(True)
