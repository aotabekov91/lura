import gizmo
from PyQt5 import QtCore

from . import mixin
from ..element import ImageQtElement

class ImageQtModel(
        mixin.Pixmap,
        mixin.UniqLocate,
        mixin.DirElement,
        gizmo.utils.Cache,
        gizmo.mixin.model.State,
        gizmo.mixin.model.Locate,
        gizmo.mixin.model.Bookmark,
        gizmo.mixin.model.Quickmark,
        gizmo.vimo.model.Model, 
        QtCore.QObject
        ):

    f='|'.join([
      'png', 
      'bmp', 
      'gif', 
      'x[bp]m',
      'p[bgp]m', 
      'jp(e){0,1}g', 
      ])

    isType=True
    kind='image'
    pattern=f'.*({f})$'
    wantView=['ImageQtView']
    element_class=ImageQtElement
