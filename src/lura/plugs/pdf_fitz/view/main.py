import gizmo
from gizmo.utils import tag
from PyQt5 import QtWidgets

from . import mixin
from ..item import FitzItem

class FitzView(
        mixin.Copy,
        mixin.Hint,
        mixin.Yank,
        mixin.Items,
        mixin.Rotate,
        mixin.Search, 
        mixin.BoxHint,
        mixin.WordHint,
        mixin.Annotate,
        mixin.LinkHint,
        mixin.BoxVisual,
        mixin.GrayScale,
        mixin.WordVisual,
        mixin.YankToCard,
        mixin.TrimMargins,
        mixin.AnnotationHint,
        mixin.RubberbandVisual,
        gizmo.mixin.view.Scale, 
        gizmo.mixin.view.State, 
        gizmo.mixin.view.ZXYPos, 
        gizmo.mixin.view.Pixmap, 
        gizmo.mixin.view.Select,
        gizmo.mixin.view.Leaper,
        gizmo.mixin.view.Locate,
        gizmo.mixin.view.SceneGo,
        gizmo.mixin.view.Bookmark,
        gizmo.mixin.view.Metadata,
        gizmo.mixin.view.Quickmark,
        gizmo.mixin.view.Fullscreen,
        gizmo.mixin.view.ItemsHighlight,
        gizmo.vimo.view.View,
        QtWidgets.QGraphicsView,
        ):

    canFollow=True
    item_class=FitzItem
    position={'FitzView': 'C|D|x'}
