from PyQt6 import QtWidgets

from plug_qt.vimo import View

from ..tab import TabView

class DockView(
        View, 
        QtWidgets.QDockWidget
        ):
    def __init__(
        self,
        loc=None,
        min_width=200,
        min_height=200,
        zoom_factor=0.1,
        objectName="DockWidget",
        **kwargs,
    ):
        self.loc = loc
        self.min_w = min_width
        self.min_h = min_height
        self.zfactor = zoom_factor
        super().__init__(objectName=objectName, **kwargs)
        self.createTab()

    @property
    def current(self):
        return self.tab.current

    @property
    def previous(self):
        return self.tab.previous

    def createTab(self):
        tab = TabView(
            parent=self,
            app=self.app,
            manager=self,
            identifier="T",
            has_tabs=False,
            tab_classes={},
            initial_create=False,
        )
        self.setWidget(tab)
        self.tab = tab
        tab.show()

    def removeView(self, view, **kwargs):
        self.hide()
        self.tab.removeView(view)

    def addView(self, view, **kwargs):
        view.setMinimumSize(self.min_w, self.min_h)
        self.tab.addView(view)
        view.setManager(self)

    def betView(self, *args, view=None, **kwargs):
        self.hide()
        self.octivate()

    def setView(self, *args, view=None, **kwargs)->None:
        self.activate()
        self.tab.setView(*args, view=view, **kwargs)
        view.resize(self.sizeHint())

    def insertView(self, idx=-1, view=None, **kwargs):
        self.tab.insertView(idx, view, **kwargs)

    def scale(self, kind, xrange=[1]):
        if self.current:
            self.zoomTo(kind, xrange)

    def zoomTo(self, kind, xrange=[1]):
        if kind == "out":
            zf = (1.0 - self.zfactor) ** xrange
        elif kind == "in":
            zf = (1.0 + self.zfactor) ** xrange
        else:
            return
        s = self.size()
        w, h = s.width(), s.height()
        c = self.current.size()
        if self.loc in ["left", "right"]:
            w = int(c.width() * zf)
            self.setFixedWidth(w)
        else:
            h = int(c.height() * zf)
            self.setFixedHeight(h)
