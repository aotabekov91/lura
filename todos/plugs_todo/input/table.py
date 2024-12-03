from plug.utils import tag


class TableWidgetInput:
    hasInput = True

    @tag("<c-i>(input)[^]")
    def toggleInputMode(self):
        m = self.app.stateman.toggle(
            mode="input", passive=["input", "any"]
        )
        if m == "normal":
            pos = self.m_curr
            if pos:
                i = self.m_layout.itemAtPosition(*pos)
                w = i.widget()
                w.setInputMode()
            else:
                v = self.app.stateman.view()
                v.setFocus()

    @tag("i(normal)[^]")
    def enterInsertMode(self):
        if self.checkProp("hasInput"):
            pos = self.m_curr
            if not pos:
                return
            i = self.m_layout.itemAtPosition(*pos)
            w = i.widget()
            if self.checkProp("canEdit", w):
                self.toggleInputMode()
                w.setInputMode(True)
