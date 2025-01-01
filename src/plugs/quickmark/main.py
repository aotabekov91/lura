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
    def setQuickmark(self):
        view=self.app.stateman.view()
        normal=self.app.plugman.getPlug('Normal')
        agent=normal.getAgent(action='goTo', view=view)
        if agent:
            self.app.stateman.activate(
                submode="mark",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.functor)

    @tag("`/''(normal)")
    def goToQuickmark(self):
        view=self.app.stateman.view()
        normal=self.app.plugman.getPlug('Normal')
        agent=normal.getAgent(action='goTo', view=view)
        if agent:
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
        normal=self.app.plugman.getPlug('Normal')
        position=normal.getState(state='goTo', view=view)
        self.saveQuickmark(view, text, position)

    def jump(self, text, view):
        normal=self.app.plugman.getPlug('Normal')
        quickmarks=self.getQuickmark(view)
        if quickmarks:
            data=quickmarks.get(text, {})
            normal.activate(action='goTo', view=view, **data)
