from plug_qt.plugs.exec import Exec

from plug_qt.plugs.search import Search

from plug_qt.plugs.overlay import Overlay
from plug_qt.plugs.editline import Editline
from plug_qt.plugs.powerline import Powerline

from plug_qt.plugs.visual import Visual
from plug_qt.plugs.visual_block import BlockVisual

from plug_qt.plugs.normal import Normal
from plug_qt.plugs.normal_tab import TabNormal
from plug_qt.plugs.normal_tile import TileNormal
from plug_qt.plugs.normal_dock import DockNormal
from plug_qt.plugs.normal_tree import TreeGoToNormal

from plug_qt.plugs.yank import Yank
from plug_qt.plugs.general import General
from plug_qt.plugs.selection import Selection
from plug_qt.plugs.outline import Outline

from plug_qt.plugs.fullscreen import Fullscreen
from plug_qt.plugs.fullscreen_tile import TileViewFullscreen
from plug_qt.plugs.fullscreen_dock import DockViewFullscreen

from plug_qt.plugs.picky import Picky


from plug_qt.plugs.grayscale import Grayscale
from plug_qt.plugs.bookmark import Bookmark
from plug_qt.plugs.bookmarks import Bookmarks
from plug_qt.plugs.bookmark_sqlite import BookmarkSQLiteTable
from plug_qt.plugs.files_tree import FilesTree
from plug_qt.plugs.quickmark import Quickmark

from plug_qt.plugs.hint import Hint
from plug_qt.plugs.hint_annotation import AnnotationHint
from plug_qt.plugs.hint_box import BoxHint
from plug_qt.plugs.hint_link import LinkHint
from plug_qt.plugs.hint_view import ViewHint
from plug_qt.plugs.hint_block import BlockHint

from plug_qt.plugs.annotate import Annotate
from plug_qt.plugs.annotation_sqlite import AnnotationSQLiteTable

from plug_qt.plugs.states import States
from plug_qt.plugs.states_sqlite import StatesSQLiteTable

from plug_qt.plugs.tabline import Tabline
from plug_qt.plugs.leaper import Leaper

# todo
# from plug_qt.plugs.core_annotation_edit import AnnotationEdit,

from plug_qt.plugs.annotations import Annotations
from plug_qt.plugs.table_sqlite import SQLiteTable

def get_base_plugs():
    return [
            Exec,
            Editline,
            Powerline,
            Search,
            Normal,
            General,
            Overlay,
            TabNormal,
            TileNormal,
            DockNormal,
            TreeGoToNormal,
            Selection,

            Picky,

            Visual,
            BlockVisual,

            Fullscreen,
            DockViewFullscreen,
            # todo: :bug: indices change
            TileViewFullscreen,

            FilesTree,
            Grayscale,

            States,
            StatesSQLiteTable,

            Tabline,
            Leaper,

            Annotate,
            Annotations,
            AnnotationSQLiteTable,

            Bookmark,
            Bookmarks,
            BookmarkSQLiteTable,

            Quickmark,

            Outline,

            Hint,
            AnnotationHint,
            BoxHint,
            LinkHint,
            ViewHint,
            BlockHint,

            Yank,

            SQLiteTable,
            ]
