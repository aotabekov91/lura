import os
import re
import hashlib

import fitz

import plug
import plug_qt
from PyQt6 import QtCore

from ..element import FitzElement
from . import mixin


class FitzModel(
    mixin.Pixmap,
    mixin.Annotate,
    mixin.UniqLocate,
    plug.utils.Cache,
    plug_qt.vimo.mixin.model.State,
    plug_qt.vimo.mixin.model.Locate,
    plug_qt.vimo.mixin.model.Elements,
    plug_qt.vimo.mixin.model.Bookmark,
    plug_qt.vimo.mixin.model.Metadata,
    plug_qt.vimo.mixin.model.Annotate,
    plug_qt.vimo.mixin.model.Quickmark,
    plug_qt.vimo.model.Model,
    QtCore.QObject,
):
    isType = True
    kind = "document"
    pattern = ".*pdf$"
    wantView = ["FitzView"]
    element_class = FitzElement

    def setup(self):
        super().setup()
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
