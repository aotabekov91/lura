from gizmo.mixin import view

class Scale(view.Scale):

    def setup(self):

        super().setup()
        self.indexChanged.connect(
                self.updateItemScale)

    def updateItemScale(self):

        m=self.scaleMode
        adj=['width', 'height','adjust']
        if m in adj:
            self.m_item.updateScaleMode(m)
