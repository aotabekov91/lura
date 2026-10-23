from .exec import Exec
from .search import Search
from .overlay import Overlay
from .editline import Editline
from .powerline import Powerline

from .general import General

from .normal import Normal
from .normal_tab import TabNormal
from .normal_tile import TileNormal
from .normal_dock import DockNormal
from .normal_tree import TreeGoToNormal

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
            ]
