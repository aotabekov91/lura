import os
import re
import hashlib

import fitz

import plug
import plug_qt
from queue import Queue
from PyQt6 import QtCore

from .utils import Task
from .element import FitzElement

class FitzModel(
    plug.utils.Cache,
    plug_qt.vimo.mixin.model.Locate,
    plug_qt.vimo.mixin.model.Elements,
    plug_qt.vimo.model.Model,
    QtCore.QObject,
):
    isType = True
    kind = "document"
    pattern = ".*pdf$"
    wantView = ["FitzView"]
    element_class = FitzElement

    modelUpdated = QtCore.pyqtSignal()
    pixmapReady = QtCore.pyqtSignal(object, object, object)

    def setup(self):
        super().setup()
        self.addCache("pixmap")
        self.m_pixmap_queue = Queue()
        self.m_pixmap_thread = QtCore.QThread()
        self.m_pixmap_task = Task(self.m_pixmap_queue)
        self.m_pixmap_task.pixmapReady.connect(self.setPixmap)
        self.m_pixmap_task.moveToThread(self.m_pixmap_thread)
        self.m_pixmap_thread.started.connect(self.m_pixmap_task.run)
        self.m_pixmap_thread.start()
        self.assignId(self.m_source)

    def getUniqLocator(
            self, 
            data={}, 
            kind=None, 
            **kwargs):
        functor = self.findLocator("getUniq", kind)
        if functor:
            return functor(data)
        data["kind"] = self.kind
        data["source_id"] = self.id()
        return self.createLocator(data)

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

    def load(self):
        if not self.isLoaded:
            s = self.m_source
            self.m_data = fitz.open(s)
            self.isLoaded = True
        super().load()

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
            self.clearCache('pixmap')
        else:
            cache = self.getCache(name='pixmap')
            for key in cache.keys():
                if idx == key.get('idx', None):
                    self.dropCache(key, 'pixmap')
                    break
        # self.modelUpdated.emit()

    def getPixmap(self, element, key):
        idx=element.index()
        pixmap = self.getCache(key, "pixmap")
        if pixmap:
            return idx, key, pixmap
        self.m_pixmap_queue.put((element, key))

    def setPixmap(self, element, key, pixmap):
        idx=element.index()
        self.setCache(key, pixmap, "pixmap")
        self.pixmapReady.emit(idx, key, pixmap)
