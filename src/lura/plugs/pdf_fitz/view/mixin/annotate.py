from functools import partial

from gizmo.utils import tag


class Annotate:
    def setup(self):
        super().setup()
        self.setAnnotationKeys()

    @tag(
        "<c-a>",
        modes=[
            "normal|^",
            "visual[any]|^",
            "annotate[any]|^",
        ],
    )
    def toggleAnnotationMode(self):
        m = self.app.earman.toggle("annotate")
        if m == "annotate":
            self.toggleAnnotateHighlightMode()
        else:
            self.updateAnnotationList()

    @tag("<escape>", modes=["annotate[any]|^"])
    def octivate(self):
        self.app.earman.toggle()

    @tag("<c-h>", modes=["annotate[any]|^"])
    def toggleAnnotateHighlightMode(self):
        m = self.app.earman.toggleSubmode("highlight")
        self.updateAnnotationList(m)

    @tag("<c-u>", modes=["annotate[any]|^"])
    def toggleAnnotateUnderlineMode(self):
        m = self.app.earman.toggleSubmode("underline")
        self.updateAnnotationList(m)

    @tag("<c-s>", modes=["annotate[any]|^"])
    def toggleAnnotateStrikeOutMode(self):
        m = self.app.earman.toggleSubmode("strike-out")
        self.updateAnnotationList(m)

    @tag("<c-r>", modes=["annotate[any]|^"])
    def toggleAnnotateCaretMode(self):
        m = self.app.earman.toggleSubmode("caret")
        self.updateAnnotationList(m)

    @tag("<c-t>", modes=["annotate[any]|^"])
    def toggleAnnotateTextMode(self):
        m = self.app.earman.toggleSubmode("text")
        self.updateAnnotationList(m)

    def updateAnnotationList(self, mode=None):
        alist = []
        if self.fitz:
            cs = self.fitz.m_annotation_colors.get(mode, {})
            for n, d in cs.items():
                key = d.get("key")
                alist += [f"[{key}] {n.title()}"]
        self.app.ui.overlay.list.updateData(alist)
        self.app.ui.overlay.list.show()

    def annotate(self, func, submode):
        s = self.selection()
        if s:
            s["akind"] = submode
            s["function"] = func
            s = self.getLocator(s, "annotation")
            self.m_model.addAnnotation(s)
            self.cleanUpSelection()
        self.toggleAnnotationMode()

    def setAnnotationKeys(self):
        fitz = self.app.modeman.plugs.pdffitz
        self.fitz = fitz
        if self.checkProp("hasAnnotationColors", fitz):
            cs = self.fitz.m_annotation_colors
            for sn, sm in cs.items():
                for name, v in sm.items():
                    n, k = v["name"], v["key"]
                    submode = f"annotate[{sn}]"
                    f = partial(
                        self.annotate,
                        func=n,
                        submode=sn,
                    )
                    f.key = k
                    f.isTagged = True
                    f.hasTaggedKey = True
                    f.canDigitalize = False
                    f.modes = [f"{submode}|^"]
                    fn = f"annotate{sn.title()}{k.title()}"
                    f.name = fn
                    f.__name__ = fn
                    setattr(f, "__name__", fn)
                    setattr(self, fn, f)
        self.app.earman.add(self, view=True)

    def openAnnotationLocator(self, data={}, center=True, **kwargs):
        b = data.get("box", None)
        p = data.get("page", None)
        v = self.app.buffman.type()
        if all([v, p, b]):
            i = v.item(p)
            tl = b[0].topLeft()
            kwargs["center"] = center
            v.goTo(p, tl.x(), tl.y(), **kwargs)
            v.select(i, data)
