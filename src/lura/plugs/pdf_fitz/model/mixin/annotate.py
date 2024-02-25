from PyQt5 import QtCore, QtGui


class Annotate:
    isAnnotated = False
    hasAnnotationColors = False

    def setup(self):
        super().setup()
        self.m_annotation_colors = {}
        self.loaded.connect(self.annotateModel)
        self.setAnnotationColors()

    def setAnnotationColors(self):
        f = self.app.moder.plugs.pdffitz
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
        e = data.get("element")
        if e:
            return e
        idx = data.get("page")
        e = self.element(idx)
        data["element"] = e
        return e

    def getAnnPage(self, data={}):
        i = data.get("item", None)
        e = data.get("element", None)
        if i and not e:
            e = i.element()
        if e:
            return e.index()

    def getAnnContent(self, data={}):
        i = data.get("item", None)
        e = data.get("element", None)
        if i and not e:
            e = i.element()
        if not e:
            return ""
        t = []
        b = data.get("box", [])
        for i in b:
            n = e.extract(box=i, kind="text")
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
