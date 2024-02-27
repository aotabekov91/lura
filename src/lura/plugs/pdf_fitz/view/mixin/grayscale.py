from gizmo.utils import tag


class GrayScale:
    convertToGrayScale = False

    @tag("c", modes=["normal|^"])
    def toggleGrayScale(self):
        for i in self.m_items.values():
            i.toggleGrayScale()
