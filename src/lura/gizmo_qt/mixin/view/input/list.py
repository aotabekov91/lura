from lura.gizmo.utils import tag


class ListWidgetInput:
    hasInput = True

    @tag("i(normal)[^]")
    def inputInsertMode(self, xrange=[1]):
        w = self.getCurrentInputWidget(xrange)
        if w:
            self.app.stateman.setMode("input")
            w.setInputMode(True)

    @tag("a(normal[any])[^]")
    def inputAppendMode(self, xrange=[1]):
        w = self.getCurrentInputWidget(xrange)
        if w:
            self.app.stateman.setMode("input")
            w.setInputMode(True, mode="append")

    def getCurrentInputWidget(self, xrange):
        idx = 1
        item = self.currentItem()
        w = self.itemWidget(item)
        for i, pos in w.widgets().values():
            if self.checkProp("canEdit", i):
                if idx == xrange:
                    return i
                idx += 1
