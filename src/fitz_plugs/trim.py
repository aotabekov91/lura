from PyQt6 import QtCore

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

    def findTrimRect(self, img):
        w = img.width
        h = img.height
        scol = img.pixel(0, 0)

        leftx = 0
        found = False
        while w > leftx:
            for y in range(h):
                pxl = img.pixel(leftx, y)
                if scol != pxl:
                    found = True
                    break
            if found:
                break
            leftx += 1

        found = False
        rightx = w - 1
        while rightx > -1:
            for y in range(h):
                pxl = img.pixel(rightx, y)
                if scol != pxl:
                    found = True
            if found:
                break
            rightx -= 1
        rightx += 1

        topy = 0
        found = False
        while h > topy:
            for x in range(w):
                pxl = img.pixel(x, topy)
                if scol != pxl:
                    found = True
                    break
            if found:
                break
            topy += 1

        bottomy = h - 1
        found = False
        while bottomy > 0:
            for x in range(w):
                pxl = img.pixel(x, bottomy)
                if scol != pxl:
                    found = True
                    break
            if found:
                break
            bottomy -= 1
        bottomy += 1
        return QtCore.QRectF(leftx, topy, rightx, bottomy)

    # def setTrim(self):
    #     if not self.m_trect:
    #         p=self.m_data.get_pixmap()
    #         trect=self.findTrimRect(p)
    #         self.m_trect=self.unify(trect)
    #         self.m_trim_trans=QtGui.QTransform()
    #         self.m_size=trect.size()

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
