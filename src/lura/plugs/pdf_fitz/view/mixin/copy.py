from gizmo.qt.mixin import view


class Copy(view.Copy):
    def copy(self, *args, **kwargs):
        pos = self.getPosition()
        mode = self.scaleMode
        c = super().copy(*args, **kwargs)
        c.goTo(*pos)
        c.setScaleMode(mode)
        return c
