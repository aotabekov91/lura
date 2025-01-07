from .exec import Exec
from .search import Search
from .editline import Editline
from .powerline import Powerline

from .normal import Normal
from .normal_dock import DockNormal
from .normal_tab import TabNormal
from .normal_tree import TreeGoToNormal
from .normal_window import WindowNormal
from .normal_window_tile import TileWindowNormal

def get_base_plugs():
    return [
            Exec,
            Editline,
            Powerline,
            Search,
            Normal,
            DockNormal,
            TabNormal,
            TreeGoToNormal,
            WindowNormal,
            TileWindowNormal
            ]
