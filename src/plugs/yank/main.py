from plug import Plug, tag

class Yank(Plug):

    @tag("y(normal)")
    def toggleHint(self):
        self.app.stateman.activate(
            mode="yank",
            delisten=True,
            passive=["yank"],
            toggle_mode=True,
            )

    @tag("<escape>/<c-[>(yank[any])")
    def finishYankMode(self):
        self.app.stateman.activate()
