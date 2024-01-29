import os
import gizmo

from . import mixin

class FileModel(
        mixin.NoIcon,
        mixin.UniqLocate,
        gizmo.mixin.model.Locate,
        gizmo.mixin.model.Bookmark,
        gizmo.mixin.model.Quickmark,
        gizmo.vimo.model.FileSystemModel
        ):

    isType=True
    kind='files'
    wantUniqView=True
    wantView=['FilesView']

    def resetConfigure(self, **kwargs):

        s=kwargs.get('source', None)
        if s: self.m_source=s
        
    @classmethod
    def isCompatible(cls, s, **kwargs):

        if type(s)!=str: return False
        return s and os.path.isdir(s)

    @classmethod
    def getSourceName(cls, s, **kwargs):
        return '/'
