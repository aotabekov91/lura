from plug import Plug, deleg

from .view import OverlayView

class Overlay(Plug):

    def setup(self):
        super().setup()
        self.m_overlays={}

    @deleg('getOverlay@(normal)')
    def getOverlay(self, view=None, **kwargs):
        if view:
            name=view.__class__.__name__
            if not view in self.m_overlays:
                overlay=self.createOverlay(view=view, **kwargs)
                self.setOverlay(view, overlay)
            return self.m_overlays.get(name)

    def setOverlay(self, view, overlay):
        if view:
            name=view.__class__.__name__
            self.m_overlays[name]=overlay

    @deleg('createOverlay@(normal)')
    def createOverlay(self, *args, **kwargs):
        return OverlayView(
                *args, app=self.app, **kwargs)
