import os
import sys
import shutil
import importlib
import collections
import typing as tp
from lura.gizmo.utils import dotdict

import git
from plug import Plug
from lura.gizmo.utils import tag
from pip._internal import main as pipmain


class Plugman(Plug):
    rtp: tp.Dict[str, str] = {}
    actions: tp.Dict[tp.Any, tp.Any] = {}
    plugs: tp.Dict[tp.Any, tp.Any] = dotdict()
    folder: str = "~"
    repos: tp.List[str] = []
    install_picks: bool = False
    rtp: tp.Dict[str, str] = {}
    base: str = "https://github.com"

    def setup(self):
        super().setup()
        self.setFolder()
        self.updateRTP()
        if self.install_picks:
            self.installPicks()

    def setFolder(self):
        self.base = os.path.expanduser(self.base)
        self.folder = os.path.expanduser(self.folder)
        self.plug_folder = self.app.createFolder(
            self.folder
        )

    def getPlugs(self, plugs=set()) -> tp.Set[tp.Any]:
        for n, f in self.rtp.items():
            if os.path.exists(f):
                sys.path.insert(0, f)
                try:
                    m = importlib.import_module(n, f)
                    k = getattr(m, "get_plug_class", None)
                    if not k:
                        continue
                    kplug = k()
                    if type(kplug) != list:
                        kplug = [kplug]
                    for i in kplug:
                        plugs.add(i)
                except Exception as e:
                    msg = "Error in plug importing: "
                    print(msg, n, e)
                    raise
        return plugs

    def load(
        self,
        plugs: tp.List[tp.Any] = [],
        params: tp.Dict[str, str] = {},
        **kwargs,
    ) -> tp.Set[tp.Any]:
        if type(plugs) != set:
            iter_func = isinstance(
                plugs, collections.abc.Iterable
            )
            if not iter_func:
                plugs = [plugs]
            plugs = set(plugs)
        for p in self.getPlugs(plugs):
            self.loadPlug(p, params)
        return plugs

    def loadPlug(
        self,
        klass: tp.Callable[[...], ...],
        params: tp.Dict[str, str] = {},
    ) -> bool:
        def isLoaded(plug_class):
            for p in self.plugs.values():
                if p.__class__ == plug_class:
                    return True
            return False

        if not isLoaded(klass):
            n = klass.__name__
            args = params.get(n, {})
            c = self.app.m_config.get(n, {})

            try:
                p = klass(app=self.app, config=c, **args)
                self.add(p)
                return p
            except Exception as e:
                print("Error in plug loading: ", n, e)
                raise

    def add(self, plug) -> None:
        n = plug.name.lower()
        self.plugs[n] = plug

    def save(
        self,
        plug: tp.Any,
        actions: tp.List[tp.Any],
    ) -> None:
        self.actions[plug] = actions

    def get(self, name) -> tp.Any:
        self.plugs.get(name)

    def updateRTP(self):
        picks = self.m_config.get("Picks", [])
        for d in picks:
            r = d.get("pick", None)
            subdirs = d.get("subdir", [])
            if not r:
                continue
            n, p, f = self.getInfo(r)
            self.rtp[n] = f
            for subdir in subdirs:
                url = f"{r}/{subdir}"
                n, p, f = self.getInfo(url)
                self.rtp[n] = f

    @tag("(exec)")
    def install(self):
        picks = self.m_config.get("Picks", [])
        for data in picks:
            repo = data.get("pick", None)
            base = data.get("base", None)
            if not repo:
                continue
            self.installRepo(repo, base)

    def getInfo(self, gid):
        t = gid.split("/")
        h, n = "", t[-1]
        if len(t) > 2:
            h = "/".join(t[1:-1])
            h += "/"
        f = f"{self.folder}/{h}"
        p = f"{f}/{n}"
        return n, p, f

    def installRepo(self, repo, base=None):
        n, p, f = self.getInfo(repo)
        self.rtp[n] = f
        base = base or self.base
        if not n in self.repos:
            self.repos += [n]
        if not os.path.exists(p):
            gpath = os.path.expanduser(repo)
            if os.path.exists(gpath):
                shutil.copy(gpath, p)
            else:
                url = f"{base}/{repo}"
                git.Repo.clone_from(url, p)
        return n, f

    @tag("(exec)")
    def installRequirements(self):
        reqs = []
        for n, p in self.rtp.items():
            p = os.path.join(p, n)
            for r in self.getReqs(p):
                if r in reqs:
                    continue
                reqs += [r]
        self.installReqs(reqs)

    def getReqs(self, path):
        reqs = []
        r = os.path.join(path, "requirements.txt")
        if os.path.exists(r):
            with open(r, "r") as f:
                for i in f.readlines():
                    reqs += [i.strip("\n")]
        return set(reqs)

    def installReqs(self, reqs):
        for r in reqs:
            pipmain(["install", r])

    def installPicks(self):
        self.install()
        self.installRequirements()

    @tag("(exec)")
    def updatePicks(self):
        for name in self.repos:
            p = os.path.join(self.folder, name)
            repo = git.Repo(p)
            repo.remotes.origin.pull()

    @tag("(exec)")
    def cleanupPicks(self):
        for d in os.listdir(self.folder):
            if not d in self.repos:
                p = os.path.join(self.folder, d)
                shutil.rmtree(p)

    @tag("(exec)")
    def reloadPicks(self):
        self.load()
