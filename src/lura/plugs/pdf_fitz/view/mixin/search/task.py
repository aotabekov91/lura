from gizmo.ui.qt import mixin
from PyQt5 import QtCore


class SearchTask(mixin.view.SearchTask):
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
