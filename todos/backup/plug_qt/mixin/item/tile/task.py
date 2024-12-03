from PyQt6 import QtCore


class Task(QtCore.QObject, QtCore.QRunnable):
    Running = 0
    Finished = 1
    Interupted = 2
    finished = QtCore.pyqtSignal()
    imageReady = QtCore.pyqtSignal("QRect", bool, "QImage")

    def __init__(self, tile):
        self.m_tile = tile
        self.m_prefetch = False
        self.m_isRunning = False
        self.m_mutex = QtCore.QMutex()
        self.m_wasCanceled = self.Running
        super().__init__(tile)
        self.setup()

    def setup(self):
        self.m_item = self.m_tile.m_item
        self.m_element = self.m_item.element()
        self.m_waitCondition = QtCore.QWaitCondition()

    def start(self, rect, prefetch):
        self.m_rect = rect
        self.m_prefetch = prefetch
        self.m_mutex.lock()
        self.m_isRunning = True
        self.m_mutex.unlock()
        self.m_wasCanceled = self.Running
        self.run()

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

    def run(self):
        r = self.m_item.rotation
        x, y = self.m_item.scaledResol()
        img = self.m_element.render(x, y, r, self.m_rect)
        img.setDevicePixelRatio(
            self.m_item.devicePixelRatio
        )
        self.imageReady.emit(
            self.m_rect, self.m_prefetch, img
        )
        self.finish()

    def finish(self):
        self.finished.emit()
        self.m_mutex.lock()
        self.m_isRunning = False
        self.m_mutex.unlock()
        self.m_waitCondition.wakeAll()
