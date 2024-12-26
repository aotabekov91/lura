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

    def getAgent(self, view=None):
        if view:
            for klass in view.__class__.__mro__:
                name=klass.__name__
                agent=self.m_agents.get(name, None)
                if agent:
                    return agent

    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        data=self.currentZoom(view)
        zoomer=self.getAgent(view=view)
        functor=getattr(view, 'zoomTo', None)
        if zoomer:
            zoomer.activate(view=view, data=data, **kwargs)
            self.zoomChanged.emit(view, data)
        elif functor:
            functor(data=data, **kwargs)

    def currentZoom(self, view):
        if not view in self.m_data:
            self.m_data[view]={
                    'round': self.zoom_round,
                    'factor': self.zoom_factor,
                    }
            zoomer=self.getAgent(view=view)
            if zoomer:
                view.resized.connect(self.updateZoom)
        return self.m_data.get(view, {})

    def updateZoom(self, view):
        zoom=self.currentZoom(view)
        mode=zoom.get('mode')
        if zoom and mode in ['width', 'height']:
            zoom['kind']=mode
            self.activate(view=view, **zoom)

    @tag("zi(normal)")
    def zoomIn(self, xrange=[1,], **kwargs):
        self.activate(kind="in", xrange=xrange, **kwargs)

    @tag("zo(normal)")
    def zoomOut(self, xrange=[1,], **kwargs):
        self.activate(kind="out", xrange=xrange, **kwargs)

    @tag("zw(normal)")
    def zoomToWidth(self, **kwargs):
        self.activate(kind="width", **kwargs)

    @tag("za(normal)")
    def zoomToAdjust(self, **kwargs):
        self.activate(kind="adjust", **kwargs)

    @tag("zh(normal)")
    def zoomToHeight(self, **kwargs):
        self.activate(kind="height", **kwargs)
