import gizmo
from gizmo.utils import tag

class TreeView(
        gizmo.ui.qt.mixin.view.Copy,
        gizmo.ui.qt.mixin.view.Fullscreen,
        gizmo.ui.qt.utils.view.TreeView,
        ):

    canCopy=True
    canFollow=True
    default_mode='normal'
    prefix_keys={'|^': '<c-.>'}
    section_ratios={0: .75, 1: .25}

    def updateHeaderRatio(self):

        w=self.size().width()
        r=self.section_ratios
        for i, v in r.items():
            self.header().resizeSection(
                    i, int(w*v))


    def setup(self):

        super().setup()
        if self.section_ratios:
            self.resized.connect(
                    self.updateHeaderRatio)

    def updateKlass(self):

        self.locator='position'
        super().updateKlass()
        locator=self.m_kwargs.get(
                'locator', 'position')
        if locator: self.locator=locator
        sr=self.m_kwargs.get(
                'section_ratios')
        if sr: self.section_ratios=sr


    @classmethod
    def isCompatible(cls, m, view_kind=None, **kwargs):
        return view_kind=='views.TreeView'

    @tag('o', modes=['normal|^'])
    def open(self, *args, **kwargs):

        i=self.currentItem()
        t=self.app.buffman.type()
        if i: t.goTo(i.data())

    @tag('d', modes=['normal|^'])
    def delete(self):

        i=self.currentItem()
        m=self.model()
        if i and m:
            e=i.element()
            m.delElement(e)
