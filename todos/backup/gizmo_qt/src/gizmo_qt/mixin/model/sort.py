class Sort:
    canSort = True
    # todo

    def setup(self):
        super().setup()
        self.m_sort_cond = None

    def clearSort(self):
        self.m_sort_cond = None

    def setSort(self, cond=None):
        if cond is None:
            self.clearSort()
        else:
            elems = self.m_elements()
