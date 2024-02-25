from gizmo.plug.utils import tag


class TrimMargins:

    @tag("t", modes=["normal|^own"])
    def toggleTrimMargins(self):

        for i in self.m_items.values():
            i.toggleTrimMargins()
