from plug import Plug
from plug.utils import tag

class Rotate(Plug):

    @tag("r(normal)[FitzView]")
    def rotateView(self, xrange=None):
        view=self.app.stateman.view()
        for item in view.m_items.values():
            if xrange is None:
                rot = item.rotation() or 0
                xrange = (rot + 90) % 360
            item.setRotation(xrange)
        view.redraw()

    @tag("R(normal)[FitzView]")
    def rotateCurrentItem(self, xrange=None):
        view=self.app.stateman.view()
        item = view.currentItem()
        if item:
            item.setRotation(xrange)
        view.redraw()
