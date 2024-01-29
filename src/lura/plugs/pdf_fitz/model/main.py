import os
import fitz
import gizmo
import hashlib
from PyQt5 import QtCore

from . import mixin
from ..element import FitzElement

class FitzModel(
        mixin.Pixmap,
        mixin.Outline,
        mixin.Annotate,
        mixin.UniqLocate,
        gizmo.utils.Cache,
        gizmo.mixin.model.State,
        gizmo.mixin.model.Locate,
        gizmo.mixin.model.Elements,
        gizmo.mixin.model.Bookmark,
        gizmo.mixin.model.Metadata,
        gizmo.mixin.model.Annotate,
        gizmo.mixin.model.Quickmark,
        gizmo.vimo.model.Model,
        QtCore.QObject,
        ):

    isType=True
    kind='document'
    pattern='.*pdf$'
    wantView=['FitzView']
    element_class=FitzElement

    def setup(self):

        super().setup()
        self.assignId(self.m_source)

    def assignId(self, source):

        if os.path.isfile(source):
            source=os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            idx=shash.hexdigest()
            self.setId(idx)

    def load(self):

        if not self.isLoaded:
            s=self.m_source
            self.m_data=fitz.open(s)
            self.isLoaded=True
        super().load()
