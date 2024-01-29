from gizmo.mixin import view

class ZXYPos(view.ZXYPos):

    def openPositionLocator(
            self, data={}, **kwargs):

        p=data.get('position')
        if p:
            _, x, y = self.parsePositionLocator(p)
            idx=self.m_item.index()
            self.goTo(idx, x, y, **kwargs)
