from gizmo.ui import qt
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
    qt.mixin.view.Scale,
    qt.mixin.view.State,
    qt.mixin.view.ZXYPos,
    qt.mixin.view.Pixmap,
    qt.mixin.view.Select,
    qt.mixin.view.Leaper,
    qt.mixin.view.Locate,
    qt.mixin.view.SceneGo,
    qt.mixin.view.Bookmark,
    qt.mixin.view.Metadata,
    qt.mixin.view.Quickmark,
    qt.mixin.view.Fullscreen,
    qt.mixin.view.ItemsHighlight,
    qt.vimo.view.View,
    QtWidgets.QGraphicsView,
):
    canFollow = True
    item_class = FitzItem
    position = {"FitzView": "C|D|x"}
