import plug_qt
from PyQt6 import QtWidgets

from ..item import FitzItem
from . import mixin

class FitzView(
    mixin.Copy,
    mixin.Hint,
    mixin.Yank,
    mixin.Items,
    mixin.Search,
    mixin.BoxHint,
    mixin.WordHint,
    mixin.Annotate,
    mixin.LinkHint,
    mixin.BoxVisual,
    mixin.WordVisual,
    mixin.YankToCard,
    mixin.TrimMargins,
    mixin.AnnotationHint,
    mixin.RubberbandVisual,
    plug_qt.vimo.mixin.view.Scale,
    plug_qt.vimo.mixin.view.State,
    plug_qt.vimo.mixin.view.ZXYPos,
    plug_qt.vimo.mixin.view.Pixmap,
    plug_qt.vimo.mixin.view.Select,
    plug_qt.vimo.mixin.view.Leaper,
    plug_qt.vimo.mixin.view.Locate,
    plug_qt.vimo.mixin.view.SceneGo,
    plug_qt.vimo.mixin.view.Bookmark,
    plug_qt.vimo.mixin.view.Metadata,
    plug_qt.vimo.mixin.view.Quickmark,
    plug_qt.vimo.mixin.view.Fullscreen,
    plug_qt.vimo.mixin.view.ItemsHighlight,
    plug_qt.vimo.view.View,
    QtWidgets.QGraphicsView,
):
    canFollow = True
    item_class = FitzItem
    position = {"FitzView": "C|x"}
