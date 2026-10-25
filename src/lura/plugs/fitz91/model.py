import os
import re
import hashlib
from queue import Queue

import fitz

from PyQt6 import QtCore

import plug_qt
from plug import Cache

from .utils import Task
from .element import FitzElement

class FitzModel(
    plug_qt.vimo.model.Model,
    QtCore.QObject,
):
    kind = "PDF"
    pattern = ".*pdf$"
    wantView = ["FitzView"]
    element_class = FitzElement

    modelUpdated = QtCore.pyqtSignal()
    loaded = QtCore.pyqtSignal(object)
    elementCreated = QtCore.pyqtSignal(object)
    pixmapReady = QtCore.pyqtSignal(object, object, object)

    def elements(self):
        if not self.m_loaded:
            self.load()
        return self.m_elements

    def sourceElement(self):
        for i, e in self.m_elements.items():
            if e.data() == self.m_source:
                return e

    def load(self):
        if not self.isLoaded:
            self.m_data = fitz.open(self.m_source)
            self.isLoaded = True
        if self.element_class:
            elements = {}
            for idx, data in enumerate(self.m_data):
                element = self.element_class(
                    data=data,
                    index=idx + 1,
                    model=self,
                )
                elements[idx + 1] = element
                self.elementCreated.emit(element)
            self.m_elements = elements
            self.loaded.emit(self)

    def setup(self):
        super().setup()
        self.m_cache=Cache()
        self.m_cache.addCache("pixmap")
        self.m_pixmap_queue = Queue()
        self.m_pixmap_thread = QtCore.QThread()
        self.m_pixmap_task = Task(self.m_pixmap_queue)
        self.m_pixmap_task.pixmapReady.connect(
                self.setPixmap)
        self.m_pixmap_task.moveToThread(
                self.m_pixmap_thread)
        self.m_pixmap_thread.started.connect(
                self.m_pixmap_task.run)
        self.m_pixmap_thread.start()
        self.assignId(self.m_source)

    def assignId(self, source):
        if os.path.isfile(source):
            source = os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, "rb") as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            idx = shash.hexdigest()
            self.setId(idx)

    @classmethod
    def isCompatible(cls, source, **kwargs):
        if type(source) != str:
            return
        if not cls.pattern:
            return
        if not os.path.exists(source):
            return
        return re.match(cls.pattern, source, re.I)

    def clearPixmapCache(self, idx=None):
        if idx is None:
            self.m_cache.clearCache('pixmap')
        else:
            cache = self.m_cache.getCache(name='pixmap')
            for key in cache.copy().keys():
                if idx == key[0]:
                    self.m_cache.dropCache(key, 'pixmap')
        self.modelUpdated.emit()

    def getPixmap(self, element, key):
        idx=element.index()
        cache_key=(idx, hash(key), id(self))
        pixmap = self.m_cache.getCache(cache_key, "pixmap")
        if pixmap:
            return idx, key, pixmap
        self.m_pixmap_queue.put((element, key))

    def setPixmap(self, element, key, pixmap):
        idx=element.index()
        cache_key=(idx, hash(key))
        cache_key=(idx, hash(key), id(self))
        self.m_cache.setCache(cache_key, pixmap, "pixmap")
        self.pixmapReady.emit(idx, key, pixmap)
