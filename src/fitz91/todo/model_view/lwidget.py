import gizmo
from gizmo.utils import tag

class ListWidgetView(
        gizmo.ui.qt.mixin.view.Copy,
        gizmo.ui.qt.mixin.view.Fullscreen,
        gizmo.ui.qt.utils.view.ListWidgetView,
        ):

    canFollow=True
    default_mode='normal'
    prefix_keys={'|^': '<c-.>'}

    def updateKlass(self):

        self.locator='position'
        super().updateKlass()
        locator=self.m_kwargs.get(
                'locator', 'position')
        if locator: 
            self.locator=locator

    @classmethod
    def isCompatible(cls, m, view_kind=None, **kwargs):
        return view_kind=='views.ListWidgetView'

    @tag('o', modes=['normal|^'])
    def openAndFocus(self, *args, **kwargs):

        self.open(*args, **kwargs)
        t=self.app.buffman.type()
        t.activate()

    @tag('O', modes=['normal|^'])
    def open(self, *args, **kwargs):

        i=self.currentItem()
        t=self.app.buffman.type()
        if i: 
            d=i.element().data()
            t.openLocator(d, kind=self.locator)

    @tag('d', modes=['normal|^'])
    def delete(self):

        i=self.currentItem()
        m=self.model()
        if i and m:
            e=i.element()
            m.delElement(e)
