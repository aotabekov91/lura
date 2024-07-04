import os
import sys
import time
import pathlib
import typing as tp

from plug import Plug
from gizmo import utils

from . import components


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
        ] = components.Plugman,
        earman: tp.Callable[[...], tp.Any] = components.Earman,
        buffman: tp.Callable[
            [...], tp.Any 
        ] = components.Buffman,
        styleman: tp.Callable[
            [...], tp.Any 
        ] = components.Styleman,
        stateman: tp.Callable[
            [...], tp.Any 
        ] = components.Stateman,
    ) -> None:
        self.buffman: components.Buffman = buffman(self)
        self.stateman: components.Stateman = stateman(self)
        self.earman: components.Earman = earman(self)
        self.plugman: components.Plugman = plugman(self)
        self.styleman: components.Styleman = styleman(self)
        self.earman.add(self.stateman)
        self.earman.add(self.styleman)
        self.earman.add(self.ui)
        self.earman.add(self)

    def setParser(self, parser=utils.Parser):
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

    @utils.tag("<c-q>(any)")
    def quit(self) -> None:
        self.appSoonQuits.emit()
        time.sleep(0.1)
        while self.waiting_to_finish:
            time.sleep(0.01)
        self.pool.clear()
        sys.exit()

    @utils.tag("<c-[>(normal)")
    def hide(self) -> None:
        if self.ui and self.canHide:
            self.ui.hide()
