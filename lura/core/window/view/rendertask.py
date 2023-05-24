import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

NotCanceled=0
CanceledNormally=1
CanceledForcibly=2


class RenderTask(QObject, QRunnable):

    finished = pyqtSignal()
    imageReady = pyqtSignal(object, 'QRect', bool, 'QImage')

    NotCanceled=0
    CanceledNormally=1
    CanceledForcibly=2

    def __init__(self, page, parent):
        super().__init__(parent)
        self.m_isRunning = False
        self.m_wasCanceled=self.NotCanceled
        self.m_page = page
        self.s_settings = parent.s_settings
        self.m_prefetch = False
        self.m_mutex=QMutex()
        self.setup()

    def setup(self):
        self.setAutoDelete(False)
        self.m_waitCondition=QWaitCondition()

    def start(self, settings, rect, prefetch):
        self.s_settings = settings
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

    def run(self):

        # def cancellationPoint(self): 
        #     if testCancellation(self.m_wasCanceled, self.m_prefetch):
        #         self.finish()
        #         return True

        image = self.m_page.render(
            self.scaledResolutionX(self.s_settings),
            self.scaledResolutionY(self.s_settings),
            self.s_settings['rotation']['currentMode'],
            self.m_rect)

        image.setDevicePixelRatio(
            self.s_settings['resolution']['devicePixelRatio'])

        # if cancellationPoint(self): return

        self.imageReady.emit(
                self.s_settings, self.m_rect, self.m_prefetch, image)

        self.finish()

    def finish(self):
        self.finished.emit()
        self.m_mutex.lock()
        self.m_isRunning = False
        self.m_mutex.unlock()
        self.m_waitCondition.wakeAll()


    def testCancellation(self, wasCanceled, prefetch):
        if prefetch:
            return wasCanceled== CanceledForcibly
        return wasCanceled!= NotCanceled

    def scaledResolutionX(self, settings):
        devicePixelRatio = settings['resolution']['devicePixelRatio']
        resolutionX = settings['resolution']['resolutionX']
        scaleFactor = settings['scaleFactor']
        return scaleFactor*devicePixelRatio*resolutionX


    def scaledResolutionY(self, settings):
        scaleFactor = settings['scaleFactor']
        devicePixelRatio = settings['resolution']['devicePixelRatio']
        resolutionY = settings['resolution']['resolutionY']
        return scaleFactor*devicePixelRatio*resolutionY

