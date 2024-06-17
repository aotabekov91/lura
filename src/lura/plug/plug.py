import os
import typing as tp
from inspect import getfile
from PyQt6 import QtCore, QtWidgets

import tomli

import os
import sys
import time
import pathlib
import typing as tp

from PyQt6 import QtCore, QtWidgets

from lura import plug
from lura.gizmo import utils

from lura.qt.plug.app import components, view



class Plug(
        QtCore.QObject
        ):
    name: str = None
    isMode: bool = False
    shortname: str = None

    def __init__(
        self,
        app: tp.Any = None,
        files: tp.Dict[str, str] = {},
        config: tp.Dict[str, tp.Any] = {},
        functions: tp.Dict[str, tp.Any] = {},
        actions: tp.Dict[tp.Tuple[str, str], tp.Any] = {},
        **kwargs,
    ) -> None:
        super().__init__()
        self.app = app
        self.files = files
        self.functions = functions
        self.actions = actions
        self.m_config = config
        self.m_kwargs = kwargs
        self.setup()

    def setName(self) -> None:
        if self.name is None:
            c = self.__class__
            self.name = c.__name__

    def setup(self) -> None:
        self.setName()
        self.updateConf()
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.updateArgs()
        self.setActions()
        if self.app and self.check('earman', self.app):
            self.app.earman.add(self)

    # def setup(self) -> None:
    #     """Setting up the components of the application"""
    #     super().setup()

        self.setupParser()
        self.setupTools()
        self.setupTimer()
        self.setupPool()
        self.setupQApp()
        self.setupParts()
        self.setupView()

    def updateConf(self) -> None:
        if self.app:
            p = self.m_config
            c = self.app.m_config
            self.m_config = c.get(self.name, {})
            self.m_config.update(p)

    def updateArgs(self) -> None:
        st = self.m_config.get("Settings", {})
        for n, s in st.items():
            kw = self.m_kwargs.get(n, {})
            if type(s) != dict:
                continue
            kw.update(s)
            st[n] = kw
        self.m_kwargs.update(st)

    def setActions(self) -> None:
        def setKeys(
            obj: tp.Any,
            keys: tp.Any,
        ) -> tp.Dict[tp.Tuple[str, str], tp.Any]:
            actions = {}
            for f, k in keys.items():
                m = getattr(obj, f, None)
                if m and hasattr(m, "__func__"):
                    func = m.__func__
                    fname = func.__name__
                    n = getattr(m, "name", fname)
                    setattr(func, "name", n)
                    if type(k) == str:
                        k = {"key": k}
                    for a, v in k.items():
                        setattr(func, a, v)
                    actions[(obj.name, m.name)] = m
            return actions

        def saveOwnKeys() -> None:
            for f in self.__dir__():
                m = getattr(self, f, None)
                if not f.startswith("__"):
                    self.functions[f] = m
                if hasattr(m, "modes"):
                    d = (self.name, m.name)
                    if not d in self.actions:
                        self.actions[d] = m

        keys = self.m_config.get("Keys", {})
        actions = setKeys(self, keys)
        self.actions.update(actions)
        saveOwnKeys()

    def setBasePath(self) -> None:
        f = getfile(self.__class__)
        a = os.path.abspath(f)
        p = os.path.dirname(a)
        self.path = p.replace("\\", "/")

    def setFiles(self) -> None:
        for f in os.listdir(self.path):
            p = f"{self.path}/{f}"
            self.files[f] = p
            if f == "config.toml":
                with open(p, "rb") as y:
                    config = tomli.load(y)
                    config.update(self.m_config)
                    self.m_config = config

    def setSettings(self) -> None:
        s = self.m_config.get("Settings", {})
        for n, v in s.items():
            setattr(self, n, v)

    def check(
        self,
        prop: str | tp.List[str] | tp.Any,
        # todo::typing: str|tp.List[str] w/o tp.Any does not work
        obj: tp.Any | None,
    ) -> bool:
        if type(prop) != list:
            prop = [prop]
        for p in prop:
            c = getattr(obj, p, False)
            if not c:
                return False
        return True


    def setupQApp(self) -> None:
        self.qapp: QtWidgets.QApplication = (
            QtWidgets.QApplication(sys.argv)
        )
        self.qapp.setApplicationName(self.name)
        self.setParent(self.qapp)

    def setupView(
        self, 
        view: tp.Any = view.AppView
    ) -> None:
        if view:
            self.ui = view(app=self)

    def setupParts(
        self,
        plugman: tp.Callable[
            [...], ...
        ] = components.Plugman,
        earman: tp.Callable[[...], ...] = components.Earman,
        buffman: tp.Callable[
            [...], ...
        ] = components.Buffman,
        styleman: tp.Callable[
            [...], ...
        ] = components.Styleman,
        stateman: tp.Callable[
            [...], ...
        ] = components.Stateman,
    ) -> None:
        self.earman: components.Earman = earman(self)
        self.stateman: components.Stateman = stateman(self)
        self.buffman: components.Buffman = buffman(self)
        self.plugman: components.Plugman = plugman(self)
        self.styleman: components.Styleman = styleman(self)
        # self.earman.add(self.stateman)
        # self.earman.add(self.styleman)
        # self.earman.add(self.buffman)
        # self.earman.add(self.plugman)
        # self.earman.add(self.ui)
        self.earman.add(self.earman)
        self.earman.add(self)

    def setupPool(self) -> None:
        self.pool: QtCore.QThreadPool = QtCore.QThreadPool()

    def setupTimer(self):
        self.timer: QtCore.QTimer = QtCore.QTimer()
        self.timer.timeout.connect(self.appIsLaunched.emit)
        self.timer.setSingleShot(True)

    def setupParser(self, parser=utils.Parser):
        if parser:
            self.parser: tp.Any = parser()

    def setupTools(self, tools=utils.dotdict):
        if tools:
            self.tools: tp.Any = tools()

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
        sys.exit(self.qapp.exec())

    @utils.tag(["<c-q>(any)", "q(normal)"])
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

    def standardEvent(self, event):
        return event
