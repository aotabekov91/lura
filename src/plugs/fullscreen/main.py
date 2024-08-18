from plug import Plug, tag

class Fullscreen(Plug):

    def setup(self):
        super().setup()
        self.m_fullscreen={}
        self.m_fullsreeners={}

    def addFullscreener(self, name, fullscreener):
        self.m_fullsreeners[name]=fullscreener

    def fullscreener(self, name):
        return self.m_fullsreeners.get(name, None)

    def isFullscreen(self, view):
        return self.m_fullscreen.get(view, False)

    def setFullscreen(self, view, cond):
        self.m_fullscreen[view]=cond

    @tag("f(normal)")
    def toggle(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        fullscreener=self.fullscreener(name)
        if fullscreener:
            if self.isFullscreen(view):
                fullscreener.octivate(view)
                self.setFullscreen(view, False)
            else:
                fullscreener.activate(view)
                self.setFullscreen(view, True)
