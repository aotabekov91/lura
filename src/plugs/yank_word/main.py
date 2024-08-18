from plug import Plug, tag

class YankWord(Plug):

    def setup(self):
        super().setup()
        self.m_yankers={}

    def addYanker(self, name, yanker):
        self.m_yankers[name]=yanker

    def yanker(self, name):
        return self.m_yankers.get(name, None)

    @tag("w(yank)")
    def yankWord(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        yanker=self.yanker(name)
        if yanker:
            yanker.yank(view)
