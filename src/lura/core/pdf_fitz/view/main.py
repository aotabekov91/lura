import plug_qt
from PyQt6 import QtWidgets

from . import mixin
from ..item import FitzItem

class FitzView(
    mixin.Copy,
    mixin.Yank,
    mixin.Items,
    mixin.Search,
    # mixin.BoxHint,
    mixin.Annotate,
    # mixin.BoxVisual,
    # mixin.WordVisual,
    mixin.YankToCard,
    # mixin.AnnotationHint,
    mixin.RubberbandVisual,
    plug_qt.vimo.mixin.view.Scale,
    plug_qt.vimo.mixin.view.State,
    plug_qt.vimo.mixin.view.ZXYPos,
    plug_qt.vimo.mixin.view.Pixmap,
    plug_qt.vimo.mixin.view.Select,
    plug_qt.vimo.mixin.view.Leaper,
    plug_qt.vimo.mixin.view.Locate,
    plug_qt.vimo.mixin.view.SceneGo,
    plug_qt.vimo.mixin.view.ItemsHighlight,
    plug_qt.vimo.view.View,
    QtWidgets.QGraphicsView,
):
    canFollow = True
    item_class = FitzItem
    position = {"FitzView": "C|x"}
