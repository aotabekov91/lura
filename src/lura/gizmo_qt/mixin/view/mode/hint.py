from lura.gizmo.utils import tag

class Hint:
    canHint: bool = True

    @tag("<escape>(hint)")
    def finishHintMode(self):
        self.app.stateman.toggle()

    @tag("<c-f>(normal/hint)")
    def toggleHintMode(self):
        self.app.stateman.toggle(
            mode="hint",
            delisten=True,
            passive=["hint"],
        )
