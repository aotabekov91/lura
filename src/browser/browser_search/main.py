import functools

from PyQt6.QtWebEngineCore import QWebEnginePage

from plug import Plug

class BrowserSearch(Plug):

    def setup(self):
        self.m_current=None
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Search')
        if holder:
            holder.addAgent('BrowserView', self)

    def activate(self, action=None, **kwargs):
        if action:
            functor=getattr(self, action, None)
            if functor:
                functor(**kwargs)

    def finishSearch(self, results, *, search, view):
        view.setFocus()
        self.m_current=results
        if search:
            self.app.stateman.activate(mode='search', submode='jump')

    def currentIndex(self):
        if self.m_current:
            return self.m_current.activeMatch()
        return 0

    def count(self):
        if self.m_current:
            return self.m_current.numberOfMatches()
        return 0

    def search(self, view=None, search=None, flags=None, **kwargs):
        if view:
            page=view.page()
            callback=functools.partial(self.finishSearch, search=search, view=view)
            if flags:
                page.findText(search, flags, resultCallback=callback)
            else:
                page.findText(search, resultCallback=callback)

    def goTo(self, kind=None, xrange=[1], **kwargs):
        flags = QWebEnginePage.FindFlag(0)
        if kind=='previous':
            flags |= QWebEnginePage.FindFlag.FindBackward
        for i in range(xrange[-1]):
            self.search(flags=flags, **kwargs)
