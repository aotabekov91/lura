from gizmo.plug.utils import tag


class GrayScale:
    convertToGrayScale = False

    @tag("c", modes=["normal|^own"])
    def toggleGrayScale(self):
        for i in self.m_items.values():
            i.toggleGrayScale()
