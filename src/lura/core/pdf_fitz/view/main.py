import plug_qt
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
    plug_qt.mixin.view.Scale,
    plug_qt.mixin.view.State,
    plug_qt.mixin.view.ZXYPos,
    plug_qt.mixin.view.Pixmap,
    plug_qt.mixin.view.Select,
    plug_qt.mixin.view.Leaper,
    plug_qt.mixin.view.Locate,
    plug_qt.mixin.view.SceneGo,
    plug_qt.mixin.view.Bookmark,
    plug_qt.mixin.view.Metadata,
    plug_qt.mixin.view.Quickmark,
    plug_qt.mixin.view.Fullscreen,
    plug_qt.mixin.view.ItemsHighlight,
    plug_qt.vimo.view.View,
    QtWidgets.QGraphicsView,
):
    canFollow = True
    item_class = FitzItem
    position = {"FitzView": "C|x"}
    # position = {"FitzView": "C|D|x"}
