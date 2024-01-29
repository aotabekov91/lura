import os, re
from gizmo import mixin
from PyQt5 import QtCore

class SearchTask(mixin.view.SearchTask):

    @QtCore.pyqtSlot()
    def run(self):

        if self.m_running and self.m_text:
            p=os.path.expanduser(self.m_text)
            self.m_text=p
            p=p.rsplit('/', 1)[0]
            if not os.path.exists(p): p='/'
            for r, d, f in os.walk(p):
                for e in f:
                    p=os.path.join(r, e)
                    if re.match(self.m_text, p):
                        self.signals.ready.emit([p])
                    if not self.m_running: 
                        self.signals.finished.emit()
                        return
            self.m_running=False
            self.signals.finished.emit()
