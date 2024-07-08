from plug import Plug
from plug.utils import tag

class TrimFitzItem:
    trim=False

    def toggleTrimMargins(self):
        self.trim = not self.trim
        self.redraw()

    def updateCacheKey(self):
        super().updateCacheKey()
        self.m_cache_key['trim']=self.trim

class TrimFitzElement:

    def renderImage(self, trim=False, **kwargs):
        # todo
        img=super().renderImage(**kwargs)
        return img

class TrimFitzView(Plug):

    def setup(self):
        super().setup()
        self.app.appSoonStarts.connect(
                self.updateFitz)

    def updateFitz(self):
        self.app.wait()
        for viewer in self.app.buffman.viewers():
            if viewer.__name__=='FitzView':
                self.updateFitzViewer(viewer)
                break
        for modeller in self.app.buffman.modellers():
            if modeller.__name__=='FitzModel':
                self.updateFitzModeller(modeller)
                break
        self.app.wait(-1)

    def updateFitzModeller(self, modeller):
        klass=modeller.element_class
        name=klass.__name__
        mro=(TrimFitzElement, klass)
        modeller.element_class=type(name, mro, {})

    def updateFitzViewer(self, viewer):
        klass=viewer.item_class
        name=klass.__name__
        mro=(TrimFitzItem, klass)
        viewer.item_class=type(name, mro, {})

    @tag("t(normal)[FitzView]")
    def toggleTrimMargins(self):
        view=self.app.stateman.view()
        for i in view.m_items.values():
            i.toggleTrimMargins()
