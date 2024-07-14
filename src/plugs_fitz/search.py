from PyQt6 import QtCore

from plug import Plug
from plug_qt.vimo.mixin import view

class SearchTask(view.SearchTask):

    @QtCore.pyqtSlot()
    def run(self):
        if self.m_text:
            items = self.m_view.getItems()
            for j, i in items:
                if not self.m_running:
                    break
                e = i.m_element
                f = e.search(self.m_text)
                if f:
                    self.reportFound(i, f)
            self.signals.finished.emit()
            self.m_running = False

    def reportFound(self, i, found):
        data = []
        e = i.element()
        for f in found:
            x, y = f.x0, f.y0
            w, h = f.width, f.height
            p = QtCore.QRectF(x, y, w, h)
            pe = e.unify(p)
            data += [(i, pe)]
        self.signals.ready.emit(data)

class FitzSearchElement:

    canSearch=True

    def setup(self):
        super().setup()
        self.m_search_cache = {}

    def search(self, txt):
        c = self.m_search_cache.get(txt, None)
        if c:
            return c
        return self.m_data.search_for(txt)

    def extract(self, rect=None, box=None, kind=None):
        if box:
            rect = self.m_norm.mapRect(box)
        if rect:
            if kind == "text":
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                r = (x, y, x + w, y + h)
                f = self.m_data.get_text("blocks", clip=r)
                if f:
                    return f[0][4]
                return ""

class FitzSearchView(view.Search):

    def setupSearchTask(self, task=SearchTask):
        super().setupSearchTask(SearchTask)

    def searchSetCurrentIndex(self, idx):
        d = self.m_search_data
        i, r = d[idx]
        if self.checkProp("canHighlight", i):
            i.highlight({"box": [r]})
        d = i.index()
        x, y = r.x(), r.y()
        self.goTo(d, x, y)
        pos = self.getBarPosition(d, x, y)
        if pos:
            c = QtCore.QPointF(*pos)
            self.centerOn(c)
        super().searchSetCurrentIndex(idx)

    def clearSearchData(self):
        self.cleanUp()
        self.cleanUpSearch()
        super().clearSearchData()

    def cleanUpSearch(self):
        if not self.m_search_data:
            return
        for i, r in self.m_search_data:
            if self.checkProp("canHighlight", i):
                i.highlight()

class FitzSearch(Plug):

    def setup(self):
        super().setup()
        self.app.appSoonStarts.connect(
                self.updateFitz)

    def updateFitz(self):
        self.app.wait()
        viewers=self.app.buffman.viewers()
        modellers=self.app.buffman.modellers()
        for name, klass in viewers.items():
            if name=='FitzView':
                self.updateFitzViewer(klass)
                break
        for name, klass in modellers.items():
            if klass.__name__=='FitzModel':
                self.updateFitzModeller(klass)
                break
        self.app.wait(-1)

    def updateFitzModeller(self, modeller):
        klass=modeller.element_class
        name=klass.__name__
        mro=(FitzSearchElement, klass)
        modeller.element_class=type(name, mro, {})

    def updateFitzViewer(self, viewer):
        name=viewer.__name__
        mro=(FitzSearchView, viewer)
        viewer=type(name, mro, {})
        self.app.buffman.addViewer('FitzView', viewer)
