from lura.gizmo.utils import tag


class Input:
    hasInput = True

    @tag("<c-i>(input)[^]")
    def toggleInputMode(self):
        m = self.app.stateman.toggle(
            mode="input", passive=["input", "any"]
        )
        if m == "normal":
            v = self.app.stateman.view()
            v.setFocus()
