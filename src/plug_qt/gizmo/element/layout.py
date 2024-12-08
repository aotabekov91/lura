from PyQt6 import QtWidgets

class Layout(QtWidgets.QGridLayout):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.m_parent=parent
        self.m_current=None
        self.m_previous=None
        self.setup()

    def setup(self):
        pass

    def setCurrentIndex(self, idx):
        if idx!=self.m_current:
            widget=self.m_parent.widget(idx=idx)
            if widget:
                self.m_previous=self.m_current
                self.m_current=idx
                widget.setFocus()

    def count(self):
        return len(self.m_parent.widgets())

    def currentIndex(self):
        return self.m_current

    def goTo(self, kind=None, xrange=[1], **kwargs):
        idx=None
        if not self.m_current:
            self.setCurrentIndex(xrange[-1])
        elif kind=='up':
            idx=self.m_current-xrange[-1]
            if idx<1: idx=self.count()
        elif kind=='down':
            idx=self.m_current+xrange[-1]
            if idx>self.count(): idx=1
        elif kind=='left':
            raise
        elif kind=='right':
            raise
        elif kind=='last':
            idx=self.count()
        elif kind=='first':
            idx=1
        if not idx is None:
            self.setCurrentIndex(idx)
