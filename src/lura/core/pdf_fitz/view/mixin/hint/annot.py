from gizmo.utils import tag
from PyQt6 import QtCore, QtWidgets


class AnnotationHint:
    @tag("<c-a>(hint[any])[^]")
    def toggleHintAnnotationMode(self):
        self.app.stateman.toggleSubmode("annotation")
        self.setupHint(functor=False, kind="annotation", hint_kind="xrange")

    @tag("<c-s>(hint[annotation])[^]")
    def selectHintedAnnotation(self, xrange, **kwargs):
        sel, match = self.getMatchedHint(xrange)
        self.selectAnnotationHint(sel)

    @tag("?(hint[annotation])[^]")
    def detailHintedAnnotation(self, xrange, **kwargs):
        sel, match = self.getMatchedHint(xrange)
        if not sel:
            return
        self.selectAnnotationHint(sel)
        ann = sel.get("annotation")
        item = sel["item"]
        if not ann:
            return
        idx = ann.data().get("id")
        dtl = f"# {idx}"
        item.setToolTip(dtl)  # todo
        item.setToolTipDuration(1500)

    @tag("<c-d>(hint[annotation])[^]")
    def removeSelectedAnnotation(self, xrange, **kwargs):
        sel, match = self.getMatchedHint(xrange)
        if not sel:
            return
        ann = sel.get("annotation")
        if not ann:
            return
        m = ann.model()
        m.delElement(ann)

    @tag("<c-e>(hint[annotation])[^]")
    def editSelectedAnnotation(self, xrange, **kwargs):
        sel, match = self.getMatchedHint(xrange)
        if not sel:
            return
        ann = sel.get("annotation")
        if not ann:
            return
        d = ann.data()
        f = d.get("function")
        n = f"OverlayInputAnnotation{f.title()}"
        i = self.app.ui.overlay.input
        i.toggle(**d, objectName=n)
        i.textModified.connect(self.updateAnnotationData)

    def updateAnnotationData(self, text):
        sel = self.selection()
        if not sel:
            return
        a = sel.get("annotation")
        m = a.model()
        d = {"text": text}
        m.updateElement(a, d)
        i = self.app.ui.overlay.input
        i.textModified.disconnect(self.updateAnnotationData)

    def selectAnnotationHint(self, sel):
        if sel:
            item = sel["item"]
            self.select(item, sel)
            e = sel["annotation"]
            m = e.model()
            m.elementWanted.emit(e)

    def getAnnotationHints(self, *args, **kwargs):
        def sort(d):
            ann = d["annotation"]
            d = ann.data()
            p = d["page"]
            b = d["box"][0]
            return p, b.y(), b.x()

        alist = []
        m = self.m_model
        if not self.checkProp("canAnnotate", m):
            return
        am = m.submodel("annotation")
        if not am:
            return
        v = self.visibleItems()
        v = {i.element(): i for i in v}
        for j, e in am.elements().items():
            d = e.data()
            elem = d["element"]
            for i in self.m_items.values():
                if i.element().index() == elem.index():  # todo
                    alist += [
                        {
                            "item": i,
                            "box": d["box"],
                            "annotation": e,
                        }
                    ]
        return sorted(alist, key=sort)
