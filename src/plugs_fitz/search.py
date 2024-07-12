import math
import fitz
import subprocess

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPointF

from plug import Plug, tag

class FitzSearchElement:

    canSearch=True

    def setup(self):
        super().setup()
        self.m_search_cache = {}

    def search(self, txt):
        c = self.m_search_cache.get(txt, None)
        if c:
            return c
        return self.m_data.search_for(txt)

    def extract(self, rect=None, box=None, kind=None):
        if box:
            rect = self.m_norm.mapRect(box)
        if rect:
            if kind == "text":
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                r = (x, y, x + w, y + h)
                f = self.m_data.get_text("blocks", clip=r)
                if f:
                    return f[0][4]
                return ""

class FitzSearch(Plug):

    def setup(self):
        super().setup()
        self.app.appSoonStarts.connect(
                self.updateFitz)

    def updateFitz(self):
        self.app.wait()
        viewers=self.app.buffman.viewers()
        modellers=self.app.buffman.modellers()
        for name, klass in viewers.items():
            if name=='FitzView':
                self.updateFitzViewer(klass)
                break
        for name, klass in modellers.items():
            if klass.__name__=='FitzModel':
                self.updateFitzModeller(klass)
                break
        self.app.wait(-1)

    def updateFitzModeller(self, modeller):
        klass=modeller.element_class
        name=klass.__name__
        mro=(FitzSearchElement, klass)
        modeller.element_class=type(name, mro, {})

    def updateFitzViewer(self, viewer):
        pass
        # klass=viewer.item_class
        # name=klass.__name__
        # mro=(FitzLinkItem, klass)
        # viewer.item_class=type(name, mro, {})
        # self.app.buffman.delViewer('FitzView')
        # name=viewer.__name__
        # mro=(FitzLinkView, viewer)
        # viewer=type(name, mro, {})
        # self.app.buffman.addViewer('FitzView', viewer)
