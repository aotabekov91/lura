from plug import Plug, tag

class Visual(Plug):

    @tag("<c-v>(normal/visual)")
    def toggleVisual(self):
        self.app.stateman.toggle(
            mode="visual",
            delisten=True,
            passive=["visual"])
