import os
import sys
import time
import pathlib
import typing as tp

from .earman import Earman
from .plugman import Plugman
from .buffman import Buffman
from .styleman import Styleman
from .stateman import Stateman

from ..plug import Plug
from ..utils import Parser, tag


class App(Plug):
    """The main application construct"""

    ui: tp.Any = None
    app_wait: int = 2
    canHide: bool = False
    waiting_to_finish: int = 0

    def setup(self) -> None:
        """Setting up the components of the application"""
        super().setup()
        self.setupApp()

    def setupApp(self):
        self.setParser()
        self.setParts()

    def setParts(
        self,
        plugman: tp.Callable[
            [...], tp.Any 
        ] = Plugman,
        earman: tp.Callable[[...], tp.Any] = Earman,
        buffman: tp.Callable[
            [...], tp.Any 
        ] = Buffman,
        styleman: tp.Callable[
            [...], tp.Any 
        ] = Styleman,
        stateman: tp.Callable[
            [...], tp.Any 
        ] = Stateman,
    ) -> None:
        self.buffman: Buffman = buffman(self)
        self.stateman: Stateman = stateman(self)
        self.earman: Earman = earman(self)
        self.plugman: Plugman = plugman(self)
        self.styleman: Styleman = styleman(self)
        self.earman.add(self.stateman)
        self.earman.add(self.styleman)
        self.earman.add(self.ui)
        self.earman.add(self)

    def setParser(self, parser=Parser):
        if parser:
            self.parser: tp.Any = parser()

    def activate(self):
        self.plugman.load()
        if self.ui:
            self.ui.show()

    def createFolder(
        self,
        path: str = None,
        parents: bool = True,
        exist_ok: bool = True,
    ) -> pathlib.Path:
        path = path or f"~/{self.name.lower()}"
        f = os.path.expanduser(path)
        path = pathlib.Path(f)
        if not os.path.exists(f):
            path.mkdir(parents=parents, exist_ok=exist_ok)
        return path

    def wait(self, delta: int) -> None:
        self.waiting_to_finish += delta

    def run(self) -> None:
        if self.ui:
            self.ui.activate()
        self.timer.start(self.app_wait)
        sys.exit(self.qapp.exec_())

    @tag("<c-q>(any)")
    def quit(self) -> None:
        self.appSoonQuits.emit()
        time.sleep(0.1)
        while self.waiting_to_finish:
            time.sleep(0.01)
        self.pool.clear()
        sys.exit()

    @tag("<c-[>(normal)")
    def hide(self) -> None:
        if self.ui and self.canHide:
            self.ui.hide()
