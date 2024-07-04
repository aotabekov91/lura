from gizmo.utils import tag


class Bookmark:
    canBookmark = True

    @tag("b(normal)[^]")
    def startBookmarkMode(self):
        m = self.m_model
        if self.checkProp("canBookmark", m):
            self.app.stateman.toggle(
                mode="bookmark",
                passive=["bookmark"],
            )
            self.setBookmark()

    @tag("<enter>/<return>(bookmark)[^]")
    def saveBookmark(self):
        t = self.app.ui.bar.text()
        data = {"text": t}
        u = self.getLocator(data=data, kind="uniq")
        p = self.getLocator(data=u, kind="position")
        self.m_model.addBookmark(p)
        self.finishBookmarkMode()

    @tag("<escape>(bookmark[any])[^]")
    def finishBookmarkMode(self):
        self.app.ui.bar.octivateEdit()
        self.app.stateman.toggle()

    def setBookmark(self):
        text = ""
        l = self.getLocator(kind="position")
        pos = l.get("position")
        e = self.m_model.getBookmark(pos, by="position")
        if e:
            text = e.data("text")
        self.app.ui.bar.activateEdit(edit=text)
