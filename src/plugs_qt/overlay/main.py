from plug import Plug

from .view import OverlayView

class Overlay(Plug):

    def setup(self):
        super().setup()
        self.m_overlays={}

    def getOverlay(self, view=None, **kwargs):
        if not view in self.m_overlays:
            overlay=self.createOverlay(view=view, **kwargs)
            self.m_overlays[view]=overlay
        return self.m_overlays.get(view)

    def setOverlay(self, name, overlay):
        self.m_overlays[name]=overlay

    def createOverlay(self, *args, **kwargs):
        return OverlayView(
                *args, app=self.app, **kwargs)
