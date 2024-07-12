import fitz
from PyQt6 import QtCore

from plug import Plug
from plug_qt.vimo import mixin

class FitzAnnotateElement(mixin.element.Annotate):

    def deannotate(self, d):
        b = d["box"][0]
        b = self.m_norm.mapRect(b)
        for a in self.m_data.annots():
            p1 = QtCore.QPointF(a.rect.x0, a.rect.y0)
            p2 = QtCore.QPointF(a.rect.x1, a.rect.y1)
            r = QtCore.QRectF(p1, p2)
            if not r.intersects(b):
                continue
            self.m_data.delete_annot(a)
            self.m_model.clearPixmapCache(idx=self.index())
            self.annotationRemoved.emit(d)
            return a

    def annotate(self, d):
        a = None
        p = self.m_data
        akind = d.get("akind", None)
        q, b = self.getAnnQuads(d)
        if akind == "highlight":
            a = p.add_highlight_annot(q)
        elif akind == "underline":
            a = p.add_underline_annot(q)
        elif akind == "strike-out":
            a = p.add_strikeout_annot(q)
        elif akind == "caret":
            if b:
                r = q[0]
                a = p.add_caret_annot(r.ul)
        elif akind == "text":
            if b:
                r = q[0]
                a = p.add_text_annot(r.ul, d.get("text", ""))
        if not a:
            return
        c = d.get("color", None)
        if c:
            s = (c.redF(), c.greenF(), c.blueF())
            a.set_colors(stroke=s)
        a.update()
        self.annotationAdded.emit(d)
        self.m_model.clearPixmapCache(idx=self.index())
        self.dataChanged.emit()

    def getAnnQuads(self, d):
        q = []
        b = d.get("box")
        if type(b) != list:
            b = [b]
        for i in b:
            i = self.m_norm.mapRect(i)
            x, y = i.x(), i.y()
            w, h = i.width(), i.height()
            ul, ur = (x, y), (x + w, y)
            ll, lr = (x, y + h), (x + w, y + h)
            q += [fitz.Quad(ul, ur, ll, lr)]
        return q, b

class FitzAnnotate(Plug):

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
        mro=(FitzAnnotateElement, klass)
        modeller.element_class=type(name, mro, {})

    def updateFitzViewer(self, viewer):
        pass
        # klass=viewer.item_class
        # name=klass.__name__
        # mro=(FitzLinkItem, klass)
        # viewer.item_class=type(name, mro, {})
        # self.app.buffman.delViewer('FitzView')
        # name=viewer.__name__
        # mro=(FitzLinkView, viewer)
        # viewer=type(name, mro, {})
        # self.app.buffman.addViewer('FitzView', viewer)
