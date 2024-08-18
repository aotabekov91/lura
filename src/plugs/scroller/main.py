from PyQt6 import QtCore

from plug import Plug, tag

class Scroller(Plug, QtCore.QObject):

    @tag('s(normal)')
    def toggleScroller(self, wait=10000):
        self.m_scrolling=not self.m_scrolling
        if self.m_scrolling:
            self.m_timer.setInterval(wait)
            self.m_timer.start()
        else:
            self.m_timer.stop()

    def setup(self):
        super().setup()
        self.m_scrolling=False
        self.setupTimer()

    def setupTimer(self):
        self.m_timer = QtCore.QTimer(self)
        self.m_timer.timeout.connect(self.scrollDown)

    def scrollDown(self):
        view=self.app.stateman.view()
        view.goToScreenDown()
