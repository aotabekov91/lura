from plug.utils import tag


class Rotate:
    @tag("r(normal)[^]")
    def rotateView(self, xrange=None):
        for item in self.m_items.values():
            if xrange is None:
                rot = item.rotation() or 0
                xrange = (rot + 90) % 360
            item.setRotation(xrange)
        self.redraw()

    @tag("R(normal)[^]")
    def rotateCurrentItem(self, xrange=None):
        item = self.currentItem()
        if item:
            item.setRotation(xrange)
        self.redraw()
