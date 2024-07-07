class ItemsHighlight:
    canHighlight = True

    def highlighted(self, idx=None):
        idx = idx or self.m_curr
        i = self.item(idx)
        if i:
            return i.selection()

    def clear(self):
        for j, i in self.getItems():
            i.highlight()
        self.redraw()
