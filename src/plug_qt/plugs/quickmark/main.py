import re

from plug import Plug, tag

class Quickmark(Plug):

    def setup(self):
        super().setup()
        self.m_quickmarks={}

    def functor(self, text, earman):
        view=self.app.stateman.view()
        submode = self.app.stateman.submode()
        if re.match("[a-zA-Z0-9]", text):
            if submode == "mark":
                self.add(text, view=view)
            elif submode == "jump":
                self.jump(text, view=view)
        self.octivate()
        return True

    @tag("m(normal)")
    def setQuickmark(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        functor=self.app.delegman.getAgent(
                mode='normal', view=view, action='goTo')
        if functor:
            self.app.stateman.activate(
                submode="mark",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.functor)

    @tag("`/''(normal)")
    def goToQuickmark(self, view=None):
        if not view:
            view=self.app.stateman.view()
        functor=self.app.delegman.getAgent(
                mode='normal', view=view, action='goTo')
        if functor:
            self.app.stateman.activate(
                submode="jump",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.functor)

    @tag("<escape>/<c-[>(quickmark)")
    def octivate(self):
        self.app.stateman.activate()

    def getQuickmark(self, view, text=None):
        if view:
            model=view.model()
            if not model in self.m_quickmarks:
                self.m_quickmarks[model]={}
            quickmarks=self.m_quickmarks.get(model)
            if text is None:
                return quickmarks
            return self.m_quickmarks.get(text, None)
        return {}

    def saveQuickmark(self, view, text, position):
        quickmarks=self.getQuickmark(view)
        if not quickmarks is None:
            quickmarks[text]=position

    def add(self, text, view):
        position=self.app.delegman.delegate(
                mode='normal', view=view, action='goToState')
        self.saveQuickmark(view, text, position)

    def jump(self, text, view):
        quickmarks=self.getQuickmark(view)
        if quickmarks:
            data=quickmarks.get(text, {})
            self.app.delegman.delegate(
                    mode='normal', action='goTo', view=view, data=data)
