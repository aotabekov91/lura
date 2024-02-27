from gizmo.utils import tag


class Rotate:
    @tag("r", modes=["normal|^own"])
    def rotateView(self, rstart=None):
        for i in self.m_items.values():
            if rstart is None:
                rot = i.rotation() or 0
                rstart = (rot + 90) % 360
            i.setRotation(rstart)
        self.redraw()

    @tag("R", modes=["normal|^own"])
    def rotateCurrentItem(self, rstart=None):
        i = self.currentItem()
        if i:
            i.setRotation(rstart)
        self.redraw()
