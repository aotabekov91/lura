from gizmo.plug import Plug
from gizmo.utils import tag

from .view import OutlineView

class Outline(Plug):

    def setup(self):

        super().setup()
        self.createView()
        self.app.stateman.viewChanged.connect(
                self.updateView)

    @tag('<tab>(normal)')
    def toggle(self):
        self.m_view.toggle()

    @tag('o(normal)[OutlineView]')
    def open(self, *args, **kwargs):

        item=self.m_view.currentItem()
        subview=self.app.stateman.subview()
        if item and item.data(): 
            subview.goTo(item.data())

    def createView(self):

        self.m_view=OutlineView(
                app=self.app,
                config=self.m_config)
        self.app.buffman.saveView(
                'OutlineView', self.m_view)
        self.app.buffman.locate(
                self.m_view)

    def updateView(self, view):

        model=view.model()
        if not model: return model
        outline_model=model.submodel('outline')
        if not outline_model: return
        self.m_view.setModel(outline_model)
