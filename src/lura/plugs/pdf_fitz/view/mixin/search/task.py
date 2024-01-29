from gizmo import mixin
from PyQt5 import QtCore

class SearchTask(mixin.view.SearchTask):

    @QtCore.pyqtSlot()
    def run(self):

        if self.m_text:
            items=self.m_view.getItems()
            for j, i in items:
                if not self.m_running: 
                    break
                e=i.m_element
                f=e.search(self.m_text)
                self.reportFound(i, f)
            self.signals.finished.emit()
            self.m_running=False

    def reportFound(self, i, found):

        if found: 
            data=[]
            for f in found:
                x, y = f.x0, f.y0
                w, h = f.width, f.height 
                p=(x, y, w, h)
                pe=i.mapToElement(p, unify=True)
                data+=[(i, pe)]
            self.signals.ready.emit(data)
