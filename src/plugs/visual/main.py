from plug import Plug, tag

class Visual(Plug):

    @tag("<c-v>(normal/visual)")
    def toggleVisual(self):
        self.app.stateman.activate(
            mode="visual",
            delisten=True,
            toggle_mode=True,
            # passive=["visual"],
            )
