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
    plug_qt.vimo.mixin.model.State,
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

    repaintWanted = QtCore.pyqtSignal()
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
        self.assignId(self.m_source)

    def getUniqLocator(
        self,
        data={},
        kind=None,
        **kwargs,
    ):
        f = self.findLocator("getUniq", kind)
        if f:
            return f(data)
        data["hash"] = self.id()
        data["kind"] = self.kind
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
    def isCompatible(cls, s, **kwargs):
        if type(s) != str:
            return
        if not cls.pattern:
            return
        if not os.path.exists(s):
            return
        return re.match(cls.pattern, s, re.I)



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
        self.repaintWanted.emit()

    def getPixmapCache(self, idx, d):
        c = self.getCache((idx, d), "pixmap_cache")
        if c:
            return idx, d, c
        self.m_pixmap_queue.put((idx, d))

    def setPixmapCache(self, idx, d, p):
        self.setCache((idx, d), p, "pixmap_cache")
        self.pixmapReady.emit(idx, d, p)
