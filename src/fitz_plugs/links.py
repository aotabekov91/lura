from PyQt6 import QtCore
from plug import Plug, tag

class FitzLinkItem:

    def setup(self):
        super().setup()
        self.m_links = None 

    def getLinks(self):
        if self.m_links is None:
            self.m_links = self.element().getLinks()
            for l in self.m_links:
                l["item"] = self
        return self.m_links

class FitzLinkElement:

    def getLinks(self):
        links=[]
        link = self.data().first_link
        while link:
            data = {}
            data["link"] = link
            top_left = QtCore.QPointF(
                    link.rect.x0, link.rect.y0)
            bottom_right = QtCore.QPointF(
                    link.rect.x1, link.rect.y1)
            rect = QtCore.QRectF(
                    top_left, bottom_right)
            data["box"] = self.unify(rect)
            links += [data]
            link = link.next
        return links

class FitzLinks(Plug):

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
        mro=(FitzLinkElement, klass)
        modeller.element_class=type(name, mro, {})

    def updateFitzViewer(self, viewer):
        klass=viewer.item_class
        name=klass.__name__
        mro=(FitzLinkItem, klass)
        viewer.item_class=type(name, mro, {})

    @tag("l(hint)[FitzView]")
    def toggleLinks(self):
        raise
