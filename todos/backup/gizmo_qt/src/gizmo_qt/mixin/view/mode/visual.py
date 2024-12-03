from gizmo.utils import tag


class Visual:
    hasVisual = True

    @tag("<c-v>/(normal/visaul)[^]")
    def toggleVisualMode(self):
        self.app.stateman.toggle(
            mode="visual",
            passive=["visual", "any"],
        )
