import gizmo 
from PyQt5 import QtWidgets

from . import mixin
from ..item import ImageQtItem

class ImageQtView(
        mixin.Copy,
        mixin.Hint,
        mixin.Sort,
        mixin.Scale, 
        mixin.ZXYPos,
        mixin.Locate,
        mixin.Slider,
        mixin.DirItem,
        mixin.BoxHint,
        mixin.BoxVisual,
        mixin.GrayScale,
        gizmo.mixin.view.Pixmap, 
        gizmo.mixin.view.Select,
        gizmo.mixin.view.SceneGo,
        gizmo.mixin.view.State, 
        gizmo.mixin.view.Leaper,
        gizmo.mixin.view.Bookmark,
        gizmo.mixin.view.Quickmark,
        gizmo.mixin.view.Fullscreen,
        gizmo.mixin.view.ItemsHighlight,
        gizmo.vimo.view.View,
        QtWidgets.QGraphicsView
        ):

    canFollow=True
    item_class=ImageQtItem
    position={'ImageQtView': 'C|D|x'}
