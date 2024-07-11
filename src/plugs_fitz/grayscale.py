from plug import Plug
from plug.utils import tag

class GrayScaleFitzItem:
    gray=False

    def toggleGrayScale(self):
        self.gray = not self.gray
        self.redraw()

    def updateCacheKey(self):
        super().updateCacheKey()
        self.m_cache_key['gray']=self.gray

class GrayScaleFitzElement:

    def renderImage(self, gray=False, **kwargs):
        img=super().renderImage(**kwargs)
        if gray:
            img.invertPixels()
        return img

class FitzGrayScale(Plug):

    def setup(self):
        super().setup()
        self.app.appSoonStarts.connect(
                self.updateFitz)

    def updateFitz(self):
        self.app.wait()
        viewers=self.app.buffman.viewers()
        modellers=self.app.buffman.modellers()
        for name, klass in viewers.items(): 
            if name=='FitzView':
                self.updateFitzViewer(klass)
                break
        for name, klass in modellers.items(): 
            if name=='FitzModel':
                self.updateFitzModeller(klass)
                break
        self.app.wait(-1)

    def updateFitzModeller(self, modeller):
        klass=modeller.element_class
        name=klass.__name__
        mro=(GrayScaleFitzElement, klass)
        modeller.element_class=type(name, mro, {})

    def updateFitzViewer(self, viewer):
        klass=viewer.item_class
        name=klass.__name__
        mro=(GrayScaleFitzItem, klass)
        viewer.item_class=type(name, mro, {})

    @tag("c(normal)[FitzView]")
    def toggleGrayScale(self):
        view=self.app.stateman.view()
        for item in view.m_items.values():
            item.toggleGrayScale()
