import re

from plug import Plug, tag

class Quickmark(Plug):

    def setup(self):
        super().setup()
        self.m_quickmarks={}
        self.m_quickmarkers={}

    def addQuickmarker(self, name, quickmarker):
        self.m_quickmarkers[name]=quickmarker

    def quickmarker(self, name):
        return self.m_quickmarkers.get(name)

    def quickmarkFunctor(self, text, ear):
        submode = self.app.stateman.submode()
        if re.match("[a-zA-Z0-9]", text):
            if submode == "mark":
                self.addQuickmark(text)
            elif submode == "jump":
                self.jumpToQuickmark(text)
        self.finishQuickmarkMode()
        return True

    @tag("m(normal)")
    def setQuickmark(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        quickmarker=self.quickmarker(name)
        if quickmarker:
            self.app.stateman.activate(
                submode="mark",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.quickmarkFunctor)

    @tag("`/''(normal)")
    def goToQuickmark(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        quickmarker=self.quickmarker(name)
        if quickmarker:
            self.app.stateman.activate(
                submode="jump",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.quickmarkFunctor)

    @tag("<escape>/<c-[>(quickmark)")
    def finishQuickmarkMode(self):
        self.app.stateman.activate()

    def quickmarks(self, view):
        model=view.model()
        if not model in self.m_quickmarks:
            self.m_quickmarks[model]={}
        return self.m_quickmarks.get(model)

    def addQuickmark(self, quickmark):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        quickmarker=self.quickmarker(name)
        if quickmarker:
            data=quickmarker.quickmark(
                    quickmark, view)
            quickmarks=self.quickmarks(view)
            quickmarks[quickmark]=data

    def jumpToQuickmark(self, quickmark):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        quickmarker=self.quickmarker(name)
        if quickmarker:
            quickmarks=self.quickmarks(view)
            data=quickmarks.get(quickmark, None)
            if data:
                quickmarker.go(data, view)
