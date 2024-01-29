import re, os
from PyQt5 import QtCore
from threading import Thread

class Signals(QtCore.QObject):

    ready = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal()

class SearchTask(QtCore.QRunnable):

    def __init__(self):

        self.m_running=False
        self.signals=Signals()
        super().__init__()

    def start(self, text):

        self.m_text=text
        self.m_running=False
        if self.m_text: 
            self.m_running=True
            self.run()

    def stop(self):
        self.m_running=False

    @QtCore.pyqtSlot()
    def run(self):

        if self.m_running:
            p=os.path.expanduser(self.m_text)
            self.m_text=p
            p=p.rsplit('/', 1)[0]
            if not os.path.exists(p): p='/'
            for r, d, f in os.walk(p):
                for e in f:
                    p=os.path.join(r, e)
                    if re.match(self.m_text, p):
                        self.signals.ready.emit(p)
                    if not self.m_running: 
                        self.signals.finished.emit()
                        return
            self.m_running=False
            self.signals.finished.emit()
