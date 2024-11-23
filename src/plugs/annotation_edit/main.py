from plug import Plug, tag

from .view import EditorView
from .overlay import OverlayView

class AnnotationEdit(Plug):

    xmargin=10
    ymargin=10

    def setup(self):
        super().setup()
        self.m_agents={}
        self.setupView()

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def view(self):
        return self.m_view

    def overlay(self):
        return self.m_overlay

    def setupView(self):
        self.m_overlay=OverlayView(
                app=self.app,
                view=self.app.view.main,
                )
        self.m_view = EditorView(
            app=self.app,
            parent=self.m_overlay,
            manager=self.m_overlay,
            objectName='AnnotationEdit',
            )
        self.m_view.m_wmap={
                'id': {'w': 'Label', 'p': '0x0x1x1'}, 
                'text' : {'w': 'TextEdit', 'p': '1x0x1x1'}}

    @tag("<c-a>(edit)")
    def activate(
            self, 
            view=None, 
            annotation=None, 
            width=250,
            height=200,
            **kwargs
            ):
        if not view:
            view=self.app.stateman.view()
        if not annotation:
            selector=self.app.plugman.getPlug('Selection')
            if selector:
                selection=selector.selection(view=view)
                if selection.__class__.__name__=='AnnotateElement':
                    annotation=selection
        if not annotation:
            raise
        agent=self.getAgent(view=view)
        if agent:
            self.app.stateman.setSubmode('annotation')
            top_left=agent.getGeometry(
                    view=view, 
                    annotation=annotation,
                    **kwargs)
            if top_left:
                self.m_view.setElement(annotation)
                self.updateViewGeometry(top_left, width, height)
                self.m_view.toggle()

    def updateViewGeometry(self, top_left, width, height):
        self.m_view.move(top_left)
        vgeometry=self.m_view.geometry()
        if width:
            vgeometry.setWidth(width)
        if height:
            vgeometry.setHeight(height)
        ogeometry=self.m_overlay.geometry()
        if not ogeometry.contains(vgeometry):
            x=vgeometry.x()
            w=vgeometry.width()
            xdelta=ogeometry.width()-x-w
            if xdelta<0:
                vgeometry.setX(x+xdelta-self.xmargin)
                vgeometry.setWidth(w)
            y=vgeometry.y()
            h=vgeometry.height()
            ydelta=ogeometry.height()-y-h
            if ydelta<0:
                vgeometry.setY(y+ydelta)
                vgeometry.setHeight(h)
        self.m_view.setGeometry(vgeometry)

    @tag("<escape><c-[>(edit[annotation])")
    def octivate(self):
        raise
