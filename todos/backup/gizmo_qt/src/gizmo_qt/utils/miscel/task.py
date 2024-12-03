from PyQt6 import QtCore


class Task(QtCore.QObject, QtCore.QRunnable):
    Running = 0
    Finished = 1
    Interupted = 2

    finished = QtCore.pyqtSignal()
    taskReady = QtCore.pyqtSignal(object)

    def __init__(
        self,
        *args,
        parent=None,
        **kwargs,
    ):
        self.args = args
        self.kwargs = kwargs
        self.m_parent = parent
        self.m_isRunning = False
        self.m_mutex = QtCore.QMutex()
        self.m_wasCanceled = self.Running
        super().__init__(parent)
        self.setup()

    def setup(self):
        self.m_waitCondition = QtCore.QWaitCondition()

    def start(self, *args, **kwargs):
        self.m_mutex.lock()
        self.m_isRunning = True
        self.m_mutex.unlock()
        self.m_wasCanceled = self.Running
        self.run()

    def run(self):
        self.finish()

    def finish(self):
        self.finished.emit()
        self.m_mutex.lock()
        self.m_isRunning = False
        self.m_mutex.unlock()
        self.m_waitCondition.wakeAll()

    def cancel(self, force=False):
        self.m_wasCanceled = self.Finished
        if force:
            self.m_wasCanceled = self.Interupted

    def wait(self):
        while self.m_isRunning:
            self.m_waitCondition.wait(self.m_mutex)

    def isRunning(self):
        return self.m_isRunning

    def wasCanceled(self):
        return self.m_wasCanceled != self.Running

    def wasCanceledNormally(self):
        return self.m_wasCanceled == self.Finished

    def wasCanceledForcibly(self):
        return self.m_wasCanceled == self.Interupted
