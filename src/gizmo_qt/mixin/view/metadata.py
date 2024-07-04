from gizmo.utils import tag


class Metadata:
    hasMetadata = True

    @tag("M(command)")
    def startMetadataMode(self):
        m = self.m_model
        if self.checkProp("hasMetadata", m):
            self.app.stateman.setMode(
                mode="metadata",
                passive=["metadata"],
            )
            self.setMetadata()

    @tag("<enter>/<return>(metadata)[^]")
    def saveMetadata(self):
        t = self.app.ui.bar.text()
        p = self.getLocator(
            kind="uniq",
            data={"field": "title", "value": t},
        )
        self.m_model.addMetadata(p)
        self.finishMetadataMode()

    @tag("<escape>(metadata[any])[^]")
    def finishMetadataMode(self):
        self.app.ui.bar.octivateEdit()
        self.app.stateman.setMode()

    def setMetadata(self):
        text = ""
        e = self.m_model.getMetadata("title", by="field")
        if e:
            text = e.data("value")
        self.app.ui.bar.activateEdit(edit=text)
