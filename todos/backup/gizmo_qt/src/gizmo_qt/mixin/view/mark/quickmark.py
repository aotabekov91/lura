import re

from gizmo.utils import tag


class Quickmark:
    canQuickmark = True

    def quickmarkFunctor(self, text, ear):
        sm = self.app.stateman.submode()
        if re.match("[a-zA-Z0-9]", text):
            if sm == "mark":
                self.addQuickmark(text)
            elif sm == "jump":
                self.jumpToQuickmark(text)
        self.finishQuickmarkMode()
        return True

    @tag("m(normal)[^]")
    def setQuickmark(self):
        m = self.m_model
        if self.checkProp("canQuickmark", m):
            self.app.stateman.toggle(
                submode="mark",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.quickmarkFunctor,
            )

    @tag("`/''(normal)[^]")
    def goToQuickmark(self):
        m = self.m_model
        if self.checkProp("canQuickmark", m):
            self.app.stateman.toggle(
                submode="jump",
                mode="quickmark",
                passive=["quickmark", "any"],
                functor=self.quickmarkFunctor,
            )

    @tag("<escape>(quickmark)[^]")
    def finishQuickmarkMode(self):
        self.app.stateman.octivate()

    def addQuickmark(self, m):
        d = {"mark": m}
        u = self.getLocator(data=d, kind="uniq")
        p = self.getLocator(data=u, kind="position")
        self.m_model.addQuickmark(p)

    def jumpToQuickmark(self, m):
        e = self.m_model.getQuickmark(m)
        if not e:
            return
        self.openLocator(e.data(), kind="position")
