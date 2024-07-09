import math
import fitz
import subprocess

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPointF

from plug import Plug, tag


class FitzLinkView:

    canHandleLinks=True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(
                self.selectLinkHint)

    def openLink(self, link):
        if not link: return
        d = link["link"].dest
        if d.kind in [fitz.LINK_GOTO, fitz.LINK_GOTOR]:
            raise
        elif d.kind in [fitz.LINK_URI]:
            cmd = ["qutebrowser", d.uri]
            subprocess.Popen(cmd)
        elif d.kind in [fitz.LINK_NAMED, fitz.LINK_LAUNCH]:
            r = self.m_model.m_data.resolve_link(d.uri)
            p, x, y = r
            if math.isnan(x): x=0.
            if math.isnan(y): y=0.
            tl = QPointF(x, y)
            item = self.item(p + 1)
            elem = item.element()
            tl = elem.unify(tl)
            self.goTo(p + 1, tl.x(), tl.y())

    def toggleLinkMode(self):
        sm = self.app.stateman.toggleSubmode("link")
        if sm == "link":
            self.setupHint("link")

    def selectLinkHint(self, kind, sel):
        if kind == "link":
            try:
                self.openLink(sel)
            except:
                pass
            self.app.stateman.toggle()

    def getLinkHints(self):
        alist = []
        for i in self.visibleItems():
            alist += i.getLinks()
        return alist

    def paintLinkHints(self, painter, ops, widget, item):
        if self.m_hinting:
            painter.save()
            m = self.m_hint_map.get(item, {})
            pen = QtGui.QPen(
                    QtCore.Qt.GlobalColor.red, 0.0)
            painter.setPen(pen)
            for text, data in m.items():
                box = data["box"]
                rect = []
                if type(box) != list:
                    box = [box]
                for l in box:
                    rect += [item.mapToItem(l, unified=True)]
                painter.drawText(rect[0].topLeft(), text)
            painter.restore()

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
        viewers=self.app.buffman.viewers()
        modellers=self.app.buffman.modellers()
        for name, klass in viewers.items():
            if name=='FitzView':
                self.updateFitzViewer(klass)
                break
        for name, klass in modellers.items():
            if klass.__name__=='FitzModel':
                self.updateFitzModeller(klass)
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
        self.app.buffman.delViewer('FitzView')
        name=viewer.__name__
        mro=(FitzLinkView, viewer)
        viewer=type(name, mro, {})
        self.app.buffman.addViewer('FitzView', viewer)

    @tag("<c-l>(hint/hint[link])[FitzView]")
    def toggleLinks(self):
        view=self.app.stateman.view()
        if self.check('canHint', view):
            view.toggleLinkMode()
