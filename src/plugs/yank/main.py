from plug import Plug, tag

class Yank(Plug):

    def setup(self):
        super().setup()
        self.m_yankers={}

    def addYanker(self, name, yanker):
        self.m_yankers[name]=yanker

    def yanker(self, name):
        return self.m_yankers.get(name, None)

    @tag("y(normal)")
    def toggleHint(self):
        self.app.stateman.toggle(
            mode="yank",
            delisten=True,
            passive=["yank"])

    @tag("<escape>(yank[any])")
    def finishYankMode(self):
        self.app.stateman.toggle()
