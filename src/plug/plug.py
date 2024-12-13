import os
import sys
import tomli
import pathlib
import typing as tp
from inspect import getfile

class Plug:

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
        self.files = files.copy()
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

    def tearup(self) -> None:
        if self.app and self.check('earman', self.app):
            self.app.earman.sub(self)

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

    def getFile(self, name):
        return self.files.get(name, None)

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
