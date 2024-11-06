from plug import tag

class Select:
    canSelect = True

    def setup(self):
        super().setup()
        self.m_selection = None
        self.cleanUpWanted.connect(self.cleanUpSelection)

    def select(self, item, data, **kwargs):
        if self.checkProp("canSelect", item):
            item.select(data, **kwargs)
            self.m_selection = data

    def selection(self):
        return self.m_selection

    def clearSelection(self):
        for item in self.m_items.values():
            if self.checkProp("canSelect", item):
                item.select()

    #todo refactor this tag to a generic class
    @tag('<c-[>(normal/visual)[FitzView]')
    def cleanUpSelection(self):
        self.clearSelection()
        self.m_selection = None
