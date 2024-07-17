import os
import sys
import git
import shutil
import importlib
import collections
import typing as tp

from ..plug import Plug
from ..utils import tag

class Picky(Plug):

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
        for plug in self.getPlugs(plugs):
            self.loadPlug(plug, params)
        return plugs

    def loadPlug(
        self,
        klass: tp.Callable[[...], tp.Any],
        params: tp.Dict[str, str] = {},
    ) -> bool:

        def isLoaded(plug_class):
            for plug in self.plugs.values():
                if plug.__class__ == plug_class:
                    return True
            return False

        if not isLoaded(klass):
            name = klass.__name__
            args = params.get(name, {})
            config = self.app.m_config.get(name, {})

            try:
                plug = klass(
                        app=self.app, 
                        config=config, 
                        **args)
                self.add(plug)
                return plug
            except Exception as e:
                print("Error in plug loading: ", name, e)
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

    def updatePlugsDict(self):
        picks = self.m_config.get("Picks", [])
        for pick in picks:
            if type(pick)==str:
                pick=dict(plug=pick)
            name=self.updateInfo(pick)
            self.plugs[name] = pick

    def updateInfo(self, pick):
        plug=pick.get('plug')
        _, repo = tuple(plug.split("/"))
        pick['repo']=repo
        return repo

    def installRepo(self, repo, base=None):
        name, path, folder = self.updateInfo(repo)
        self.plugs[name] = folder
        base = base or self.base
        if not name in self.repos:
            self.repos += [name]
        if not os.path.exists(path):
            gpath = os.path.expanduser(repo)
            if os.path.exists(gpath):
                shutil.copy(gpath, path)
            else:
                url = f"{base}/{repo}"
                git.Repo.clone_from(url, path)
        return name, folder

    # def getPlugs(self, plugs=set()) -> tp.Set[tp.Any]:
    #     for name, folder in self.plugs.items():
    #         if os.path.exists(folder):
    #             sys.path.insert(0, folder)
    #             try:
    #                 m = importlib.import_module(name, folder)
    #                 k = getattr(m, "get_plug_class", None)
    #                 if not k:
    #                     continue
    #                 kplug = k()
    #                 if type(kplug) != list:
    #                     kplug = [kplug]
    #                 for i in kplug:
    #                     plugs.add(i)
    #             except Exception as e:
    #                 msg = "Error in plug importing: "
    #                 print(msg, name, e)
    #                 raise
    #     return plugs

    # def loadPicks(self):

    def getPlugs(self, plugs=set()) -> tp.Set[tp.Any]:

        sys.path.insert(0, self.folder)
        for name in os.listdir(self.folder):
            try:
                module = importlib.import_module(name)
                klasser = getattr(module, "get_plug_class", None)
                if not klasser:
                    continue
                plugger = klasser()
                if type(plugger) != list:
                    plugger = [plugger]
                for plug in plugger:
                    plugs.add(plug)
            except Exception as e:
                msg = "Error in plug importing: "
                print(msg, name, e)
                raise
        return plugs

    @tag("(exec)")
    def installPicks(self):
        self.updatePlugsDict()
        picks = self.m_config.get("Picks", [])
        for data in picks:
            repo = data.get("pick", None)
            base = data.get("base", None)
            if not repo:
                continue
            self.installRepo(repo, base)

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
