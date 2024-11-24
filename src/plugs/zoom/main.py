from PyQt6 import QtCore

from plug import Plug, tag

class Zoom(Plug, QtCore.QObject):

    zoom_round=3
    zoom_factor = 0.05
    zoomChanged = QtCore.pyqtSignal(object, object)

    def setup(self):
        super().setup()
        self.m_data={}
        self.m_agents={}

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag("zi(normal)")
    def zoomIn(self, xrange=[1,], **kwargs):
        self.zoomTo(kind="in", xrange=xrange, **kwargs)

    @tag("zo(normal)")
    def zoomOut(self, xrange=[1,], **kwargs):
        self.zoomTo(kind="out", xrange=xrange, **kwargs)

    @tag("zw(normal)")
    def zoomToWidth(self, **kwargs):
        self.zoomTo(kind="width", **kwargs)

    @tag("za(normal)")
    def zoomToAdjust(self, **kwargs):
        self.zoomTo(kind="adjust", **kwargs)

    @tag("zh(normal)")
    def zoomToHeight(self, **kwargs):
        self.zoomTo(kind="height", **kwargs)

    def currentZoom(self, view):
        if not view in self.m_data:
            self.m_data[view]={
                    'round': self.zoom_round,
                    'factor': self.zoom_factor,
                    }
            zoomer=self.getAgent(view=view)
            if zoomer:
                view.resized.connect(self.updateZoom)
        return self.m_data.get(view)

    def updateZoom(self, view):
        zoom=self.currentZoom(view)
        mode=zoom.get('mode')
        if mode in ['width', 'height']:
            zoom['kind']=mode
            self.zoomTo(view=view, **zoom)

    def zoomTo(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        zoomer=self.getAgent(view=view)
        if zoomer:
            data=self.currentZoom(view)
            zoomer.activate(view=view, data=data, **kwargs)
            self.zoomChanged.emit(view, data)
