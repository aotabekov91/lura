from PyQt6 import QtCore


class Signals(QtCore.QObject):
    ready = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal()


class SearchTask(QtCore.QRunnable):
    def __init__(self):
        self.m_text = None
        self.m_running = False
        self.signals = Signals()
        super().__init__()

    def start(self, text=None, view=None):
        self.m_running = False
        self.m_text = text
        self.m_view = view
        self.m_running = True
        self.run()

    @QtCore.pyqtSlot()
    def run(self):
        self.signals.finished.emit()
        self.m_view = None
        self.m_running = False
