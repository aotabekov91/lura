import gizmo_qt
from PyQt6 import QtWidgets

from ..item import FitzItem
from . import mixin


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
    gizmo_qt.mixin.view.Scale,
    gizmo_qt.mixin.view.State,
    gizmo_qt.mixin.view.ZXYPos,
    gizmo_qt.mixin.view.Pixmap,
    gizmo_qt.mixin.view.Select,
    gizmo_qt.mixin.view.Leaper,
    gizmo_qt.mixin.view.Locate,
    gizmo_qt.mixin.view.SceneGo,
    gizmo_qt.mixin.view.Bookmark,
    gizmo_qt.mixin.view.Metadata,
    gizmo_qt.mixin.view.Quickmark,
    gizmo_qt.mixin.view.Fullscreen,
    gizmo_qt.mixin.view.ItemsHighlight,
    gizmo_qt.vimo.view.View,
    QtWidgets.QGraphicsView,
):
    canFollow = True
    item_class = FitzItem
    position = {"FitzView": "C|D|x"}
