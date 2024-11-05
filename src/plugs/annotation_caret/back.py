from functools import partial

from plug import Plug, tag

class Annotate(Plug):

    def setup(self):
        super().setup()
        self.m_annotators={}
        self.setAnnotationKeys()

    def addAgent(self, name, annotator):
        self.m_annotators[name]=annotator

    def annotator(self, name):
        return self.m_annotators.get(name, None)

    @tag(["<c-a>(normal)", "<c-a>/<c-[>(annotate)"])
    def toggle(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        annotator=self.annotator(name)
        if annotator:
            mode = self.app.stateman.toggle("annotate")
            if mode == "annotate":
                annotator.activate(view)
            else:
                annotator.octivate(view)

    @tag("<escape>(annotate[any])")
    def octivate(self):
        self.app.stateman.toggle()

    @tag("<c-h>(annotate[any])")
    def toggleAnnotateHighlightMode(self):
        m = self.app.stateman.toggleSubmode("highlight")
        self.updateAnnotationList(m)

    @tag("<c-u>(annotate[any])")
    def toggleAnnotateUnderlineMode(self):
        m = self.app.stateman.toggleSubmode("underline")
        self.updateAnnotationList(m)

    @tag("<c-s>(annotate[any])")
    def toggleAnnotateStrikeOutMode(self):
        m = self.app.stateman.toggleSubmode("strike-out")
        self.updateAnnotationList(m)

    @tag("<c-r>(annotate[any])")
    def toggleAnnotateCaretMode(self):
        m = self.app.stateman.toggleSubmode("caret")
        self.updateAnnotationList(m)

    @tag("<c-t>(annotate[any])")
    def toggleAnnotateTextMode(self):
        m = self.app.stateman.toggleSubmode("text")
        self.updateAnnotationList(m)

    def setAnnotationKeys(self):
        fitz = self.app.plugman.plugs.pdffitz
        self.fitz = fitz
        if self.checkProp("hasAnnotationColors", fitz):
            cs = self.fitz.m_annotation_colors
            for sn, sm in cs.items():
                for name, v in sm.items():
                    n, k = v["name"], v["key"]
                    f = partial(
                        self.annotate,
                        func=n,
                        submode=sn,
                    )
                    f.key = f"{k}(annotate[{sn}])"
                    f.isTagged = True
                    f.hasTaggedKey = True
                    f.canDigitalize = False
                    fn = f"annotate{sn.title()}{k.title()}"
                    f.name = fn
                    f.__name__ = fn
                    setattr(f, "__name__", fn)
                    setattr(self, fn, f)
        self.app.earman.add(self)
