import math

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

NotCanceled=0
CanceledNormally=1
CanceledForcibly=2

class Task(QObject, QRunnable):

    finished = pyqtSignal()
    imageReady = pyqtSignal('QRect', bool, 'QImage')

    NotCanceled=0
    CanceledNormally=1
    CanceledForcibly=2

    def __init__(self, parent):
        super().__init__(parent)
        self.m_prefetch = False
        self.m_isRunning = False
        self.m_wasCanceled=self.NotCanceled
        self.m_mutex=QMutex()
        self.setup()

    def setup(self):
        self.setAutoDelete(False)
        self.m_waitCondition=QWaitCondition()

    def start(self, rect, prefetch):
        self.m_rect = rect
        self.m_prefetch = prefetch
        self.m_mutex.lock()
        self.m_isRunning = True
        self.m_mutex.unlock()
        self.m_wasCanceled=self.NotCanceled
        # QThreadPool.globalInstance().start(self, int(~prefetch))
        # QThreadPool.globalInstance().start(self)
        self.run()

    def setAutoDelete(self, condition):
        pass

    def cancel(self, force=False):
        self.m_wasCanceled=self.CanceledNormally
        if force:
            self.m_wasCanceled=self.CanceledForcibly

    def wait(self):
        mutexLocker=QMutexLocker(self.m_mutex)
        while self.m_isRunning:
            self.m_waitCondition.wait(self.m_mutex)

    def isRunning(self):
        mutexLocker = QMutexLocker(self.m_mutex)
        return self.m_isRunning

    def wasCanceled(self):
        return self.m_wasCanceled!=self.NotCanceled

    def wasCanceledNormally(self):
        return self.m_wasCanceled==self.CanceledNormally

    def wasCanceledForcibly(self):
        return self.m_wasCanceled==self.CanceledForcibly

    def page(self):
        return self.parent().pageItem().page()

    def pageItem(self):
        return self.parent().pageItem()

    def run(self):

        image = self.page().render(
            self.pageItem().scaledResolutionX(),
            self.pageItem().scaledResolutionY(),
            self.pageItem().rotation(),
            self.m_rect)

        image.setDevicePixelRatio(self.pageItem().devicePixelRatio())
        self.imageReady.emit(self.m_rect, self.m_prefetch, image)
        self.finish()

    def finish(self):
        self.finished.emit()
        self.m_mutex.lock()
        self.m_isRunning = False
        self.m_mutex.unlock()
        self.m_waitCondition.wakeAll()
