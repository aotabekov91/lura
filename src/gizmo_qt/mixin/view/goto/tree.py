from app.utils import tag

from .view import ViewGo


class TreeGo(ViewGo):
    def goTo(self, xrange=None, **kwargs):
        if xrange is None:
            super().goToLastSibling()
        else:
            i = self.currentIndex()
            p = i.parent()
            row = xrange[-1] - 1
            if p.isValid():
                n = p.child(row, 0)
            else:
                n = self.m_model.index(row, 0)
            self.setCurrentIndex(n)

    def getRowIndex(self, row):
        idx = self.currentIndex()
        pidx = idx.parent()
        return pidx.child(row, 0)

    def goToRight(self, **kwargs):
        super().expand()

    def goToLeft(self, **kwargs):
        super().collapse()

    @tag("gp(normal)[TreeView]")
    def goToParent(self, xrange=[1], **kwargs):
        super().goToParent(xrange, **kwargs)

    @tag("<c-j>(normal)[TreeView]")
    def goToSiblingDown(self, xrange=[1], **kwargs):
        super().goToSiblingDown(xrange)

    @tag("<c-k>(normal)[TreeView]")
    def goToSiblingUp(self, xrange=[1], **kwargs):
        super().goToSiblingUp()

    @tag("E(normal)[TreeView]")
    def expandAll(self):
        super().expandAll()

    @tag("C(normal)[TreeView]")
    def collapseAll(self):
        super().collapseAll()
        self.goToFirst()

    @tag("H(normal)[TreeView]")
    def collapseAllInside(self):
        super().collapseAllInside()

    @tag("d(normal)[TreeView]")
    def rootDown(self, xrange=[1]):
        super().rootDown(xrange)

    @tag("u(normal)[TreeView]")
    def rootUp(self, xrange=[1]):
        super().rootUp(xrange)
