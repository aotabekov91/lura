from queue import Queue

from PyQt6 import QtCore

from .task import Task


class Pixmap:
    modelUpdated = QtCore.pyqtSignal()
    pixmapReady = QtCore.pyqtSignal(object, object, object)

    def setup(self):
        super().setup()
        self.addCache("pixmap_cache")
        self.m_pixmap_queue = Queue()
        self.m_pixmap_thread = QtCore.QThread()
        self.m_pixmap_task = Task(self, self.m_pixmap_queue)
        self.m_pixmap_task.pixmapReady.connect(self.setPixmapCache)
        self.m_pixmap_task.moveToThread(self.m_pixmap_thread)
        self.m_pixmap_thread.started.connect(self.m_pixmap_task.run)
        self.m_pixmap_thread.start()

    def clearPixmapCache(self, idx=None):
        if idx is None:
            self.clearCache("pixmap_cache")
        else:
            m = []
            name = "pixmap_cache"
            c = self.getCache(name=name)
            alist = list(c.keys())
            for i in alist:
                if idx in i:
                    self.dropCache(i, name)
        self.modelUpdated.emit()

    def getPixmapCache(self, idx, d):
        c = self.getCache((idx, d), "pixmap_cache")
        if c:
            return idx, d, c
        self.m_pixmap_queue.put((idx, d))

    def setPixmapCache(self, idx, d, p):
        self.setCache((idx, d), p, "pixmap_cache")
        self.pixmapReady.emit(idx, d, p)
