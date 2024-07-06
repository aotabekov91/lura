from app.utils import tag


class Rotate:
    @tag("r(normal)[^]")
    def rotateView(self, xrange=None):
        for i in self.m_items.values():
            if xrange is None:
                rot = i.rotation() or 0
                xrange = (rot + 90) % 360
            i.setRotation(xrange)
        self.redraw()

    @tag("R(normal)[^]")
    def rotateCurrentItem(self, xrange=None):
        i = self.currentItem()
        if i:
            i.setRotation(xrange)
        self.redraw()
