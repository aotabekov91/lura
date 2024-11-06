from plug import Plug, tag

class Yank(Plug):

    @tag("y(normal)")
    def toggleHint(self):
        self.app.stateman.toggle(
            mode="yank",
            delisten=True,
            passive=["yank"])

    @tag("<escape>/<c-[>(yank[any])")
    def finishYankMode(self):
        self.app.stateman.toggle()
