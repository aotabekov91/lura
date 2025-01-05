from PyQt6 import QtCore

from plug import Plug, tag

class Scroller(Plug, QtCore.QObject):

    def setup(self):
        super().setup()
        self.m_scrolling=False
        self.setupTimer()

    @tag('s(normal)')
    def toggleScroller(self, xrange=[1], **kwargs):
        wait=6000*xrange[-1]
        self.m_scrolling=not self.m_scrolling
        if self.m_scrolling:
            self.m_timer.setInterval(wait)
            self.m_timer.start()
        else:
            self.m_timer.stop()

    def setupTimer(self):
        self.m_timer = QtCore.QTimer(self)
        self.m_timer.timeout.connect(self.scrollDown)

    def scrollDown(self, view=None):
        if not view:
            view=self.app.stateman.view()
        self.app.delegman.delegate(
                mode='normal', 
                view=view, 
                action='goTo', 
                kind='blockdown')
