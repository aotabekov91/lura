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
    def zoomIn(self, xrange=[1,]):
        self.setZoom(kind="in", xrange=xrange)

    @tag("zo(normal)")
    def zoomOut(self, xrange=[1,]):
        self.setZoom(kind="out", xrange=xrange)

    @tag("zw(normal)")
    def zoomToWidth(self):
        self.setZoom(kind="width")

    @tag("za(normal)")
    def zoomToAdjust(self):
        self.setZoom(kind="adjust")

    @tag("zh(normal)")
    def zoomToHeight(self):
        self.setZoom(kind="height")

    def data(self, view):
        if not view in self.m_data:
            self.m_data[view]={
                    'zoom_round': self.zoom_round,
                    'zoom_factor': self.zoom_factor,
                    }
        return self.m_data.get(view)

    def setZoom(self, kind, xrange=[1,]):
        view=self.app.stateman.view()
        zoomer=self.getAgent(view=view)
        if zoomer:
            data=self.data(view)
            zoomer.activate(view, kind, xrange, data)
