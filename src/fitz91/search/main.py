from plug import Plug, tag

class Search(Plug):

    def setup(self):
        super().setup()
        self.m_searchers={}

    def addSearcher(self, name, plug):
        self.m_searchers[name]=plug

    def getSearcher(self, view=None, name=None):
        name=name or view.__class__.__name__
        return self.m_searchers.get(name, None)

    @tag("{/}(normal)")
    def toggleSearchMode(self):
        view=self.app.stateman.view()
        searcher=self.getSearcher(view)
        if searcher:
            mode = self.app.stateman.toggle(
                mode="search", passive=["search"])
            if mode=='search':
                self.activateSearchBar()
            else:
                self.updateInfo(clear=True)

    @tag("j(search[jump])")
    def next(self, xrange=[1]):
        text = self.app.ui.bar.text()
        view=self.app.stateman.view()
        searcher=self.getSearcher(view)
        if searcher:
            searcher.go(
                    view=view,
                    text=text,
                    kind="next", 
                    xrange=xrange)
            self.updateInfo(text=text, view=view)

    @tag("k(search[jump])")
    def prev(self, xrange=[1]):
        text = self.app.ui.bar.text()
        view=self.app.stateman.view()
        searcher=self.getSearcher(view)
        if searcher:
            searcher.go(
                    view=view,
                    text=text,
                    kind="prev", 
                    xrange=xrange)
            self.updateInfo(text=text, view=view)

    @tag("gg(search[jump])")
    def first(self, xrange=[1]):
        text = self.app.ui.bar.text()
        view=self.app.stateman.view()
        searcher=self.getSearcher(view)
        if searcher:
            searcher.go(
                    view=view,
                    text=text,
                    kind="first", 
                    xrange=xrange
                    )

    @tag("G(search[jump])")
    def last(self, xrange=[1]):
        text = self.app.ui.bar.text()
        view=self.app.stateman.view()
        searcher=self.getSearcher(view)
        if searcher:
            searcher.go(
                    view=view,
                    text=text,
                    kind="last", 
                    xrange=xrange)

    @tag("{/}(search[jump])")
    def activateSearchBar(self):
        self.updateInfo(clear=True)
        self.app.stateman.setSubmode()
        self.app.ui.bar.activateEdit("/", keep=True)

    @tag("<c-[>/<escape>(search[any])")
    def octivateSearchMode(self):
        self.updateInfo(clear=True)
        self.app.ui.bar.octivateEdit()
        self.app.stateman.toggle()
        text = self.app.ui.bar.text()
        view=self.app.stateman.view()
        searcher=self.getSearcher(view)
        searcher.cleanUp(text, view)

    @tag("<return>(search)")
    def startSearch(self):
        view=self.app.stateman.view()
        view.setFocus()
        self.app.stateman.setSubmode("jump")
        searcher=self.getSearcher(view)
        text = self.app.ui.bar.text()
        data=searcher.search(text, view)
        if data: self.next()

    def updateInfo(
            self, 
            text=None,
            view=None,
            clear=False,
            ):
        info = None
        searcher=self.getSearcher(view)
        if not clear and searcher:
            count = searcher.count(text, view)
            idx = searcher.currentIndex(text, view)
            info = f"{idx+1}/{count}"
        self.app.ui.bar.setInfo(info)
