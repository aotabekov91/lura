import fitz
from PyQt6 import QtCore, QtGui

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

class FitzAnnotateModel:

    isAnnotated = False
    hasAnnotationColors = False

    def setup(self):
        super().setup()
        self.m_annotation_colors = {}
        self.loaded.connect(self.annotateModel)
        self.setAnnotationColors()

    def setAnnotationColors(self):
        f = self.app.plugman.plugs.pdffitz
        self.fitz = f
        if self.checkProp("hasAnnotationColors", f):
            return
        if f:
            c = f.m_config
            ac = c.get("Annotate", {})
            cs = ac.get("colors", {})
            f.m_annotation_colors = cs
            dc = ac.get("default_color", "green")
            f.m_annotation_default = QtGui.QColor(dc)
            for sn, sm in cs.items():
                for k, v in sm.items():
                    c = v["color"]
                    v["color"] = QtGui.QColor(c)
            f.hasAnnotationColors = True

    def annotateModel(self):
        m = self.submodel("annotation")
        if not m:
            return
        if self.isAnnotated:
            return
        elems = m.elements()
        self.clearCache("pixmap_cache")
        for e in elems.values():
            self.setAnnotationLocator(elem=e)
        m.elementAdded.connect(self.setElementAnnotation)
        m.elementRemoved.connect(self.removeElementAnnotation)
        self.isAnnotated = True

    def setElementAnnotation(self, e):
        self.setAnnotationLocator(elem=e)

    def removeElementAnnotation(self, e):
        self.delAnnotationLocator(elem=e)

    def setAnnColor(self, data):
        k = data.get("akind")
        f = data.get("function").lower()
        cs = self.fitz.m_annotation_colors.get(k)
        fcs = cs.get(f, {})
        c = fcs.get("color")
        c = c or self.fitz.m_annotation_default
        data["color"] = c
        return c

    def setAnnotationLocator(
        self,
        data={},
        elem=None,
        annotate=True,
    ):
        if elem:
            data = elem.data()
        if data:
            self.setAnnBox(data)
            self.setAnnColor(data)
            self.setAnnElement(data)
            if annotate:
                self.setElementAnn(data)
        return self.createLocator(data)

    def delAnnotationLocator(
        self,
        data={},
        elem=None,
    ):
        if elem:
            data = elem.data()
        if data:
            idx = data.get("id", None)
            e = self.setAnnElement(data)
            if e:
                e.deannotate(data)
            return self.createLocator({"id": idx})
        return self.createLocator(data)

    def getAnnotationLocator(
        self,
        data={},
        elem=None,
    ):
        if elem:
            data = elem.data()
        if data:
            data["hash"] = self.id()
            data["kind"] = self.kind
            data["position"] = self.getAnnLocation(data)
            data["content"] = self.getAnnContent(data)
            data["text"] = data["content"]
        return self.createLocator(data)

    def setElementAnn(self, data):
        b = data["element"]
        b.annotate(data)
        b.dataChanged.emit()

    def setAnnBox(self, data={}):
        b = data.get("box", None)
        p = data.get("page", None)
        if p:
            return p, b
        t = []
        ploc = data["position"]
        s = ploc.split("|", 1)
        p, loc = int(s[0]), s[1]
        for i in loc.split("_"):
            f = float
            r = QtCore.QRectF
            x, y, w, h = tuple(i.split(":"))
            t += [r(f(x), f(y), f(w), f(h))]
        data["page"], data["box"] = p, t
        return p, t

    def setAnnElement(self, data={}):
        element = data.get("element")
        if element:
            return element
        idx = data.get("page")
        element = self.element(idx)
        data["element"] = element
        return element

    def getAnnPage(self, data={}):
        item = data.get("item", None)
        element = data.get("element", None)
        if item and not element:
            element = item.element()
        if element:
            return element.index()

    def getAnnContent(self, data={}):
        item = data.get("item", None)
        element = data.get("element", None)
        if item and not element:
            element = item.element()
        if not element:
            return ""
        t = []
        b = data.get("box", [])
        for item in b:
            n = element.extract(box=item, kind="text")
            t += [n.strip("\n")]
        return " ".join(t)

    def getAnnLocation(self, data={}):
        t = []
        p = self.getAnnPage(data)
        data["page"] = p
        b = data.get("box", [])
        for i in b:
            x = str(i.x())[:6]
            y = str(i.y())[:6]
            w = str(i.width())[:6]
            h = str(i.height())[:6]
            t += [f"{x}:{y}:{w}:{h}"]
        loc = "_".join(t)
        return f"{p}|{loc}"

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
        name=modeller.__name__
        mro=(FitzAnnotateModel, modeller)
        modeller=type(name, mro, {})
        self.app.buffman.addViewer('FitzModel', modeller)

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
