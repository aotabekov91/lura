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

    running=False
    ui: tp.Any = None
    wants_to_wait: int=0
    canHide: bool = False

    def setup(self) -> None:
        """Setting up the components of the application"""
        super().setup()
        self.setupApp()

    def setupApp(self):
        self.setupParser()
        self.setupParts()

    def setupParts(
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

         self.earman: Earman = earman(self)
         self.stateman: Stateman = stateman(self)
         self.buffman: Buffman = buffman(self)
         self.plugman: Plugman = plugman(self)
         self.styleman: Styleman = styleman(self)
         self.earman.add(self.earman)
         self.earman.add(self)

    def setupParser(self, parser=Parser):
        if parser:
            self.parser: tp.Any = parser()

    def activate(self):
        self.plugman.loadPlugs()
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

    def wait(self, delta: int=1) -> None:
         self.wants_to_wait += delta

    def startUI(self):
         time.sleep(0.1)
         while self.wants_to_wait:
             time.sleep(0.01)
         if self.ui:
             self.ui.activate()

    def run(self) -> None:
         self.startUI()
         self.running=True
         sys.exit(self.qapp.exec())

    def standardEvent(self, event):
         return event

    @tag("<c-q>(any)")
    def quit(self) -> None:
        self.appSoonQuits.emit()
        time.sleep(0.1)
        while self.wants_to_wait:
            time.sleep(0.01)
        sys.exit()

    @tag("<c-[>(normal)")
    def hide(self) -> None:
        if self.ui and self.canHide:
            self.ui.hide()
