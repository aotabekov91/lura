import os
import sys
import importlib
import typing as tp
import pkg_resources
from pip._internal.cli.main import main

from ..plug import Plug
from ..utils import dotdict

class Plugman(Plug):

    folder: str = "~"
    path_plugs={}
    pip_command='install -q'
    added: tp.List[tp.Any]=[]
    plugs: tp.Dict[tp.Any, tp.Any] = dotdict()

    def setup(self):
        super().setup()
        self.setFolder()

    def setFolder(self):
        self.folder = os.path.expanduser(self.folder)
        autorun=os.path.join(self.folder, 'autorun')
        self.autorun = self.app.createFolder(autorun)

    def addPlugs(self, plugs=[]):
        self.added+=plugs

    def loadPlugs(self, params={}, folder=None, modules=[]):
        folder=folder or self.autorun
        klasses, paths=self.getPlugs(folder, modules)
        klasses=klasses.union(set(self.added))
        self.loadKlasses(klasses, paths, params)

    def loadKlasses(self, klasses, paths={}, params={}):
        for klass in klasses: 
            path=paths.get(klass, None)
            if not path in self.path_plugs:
                self.path_plugs[path]=[]
            name = klass.__name__
            plug=self.loadPlug(klass, params)
            if plug:
                self.plugs[name] = plug
                self.path_plugs[path]+=[plug]

    def isLoaded(self, plug_class):
        for plug in self.plugs.values():
            if plug.__class__ == plug_class:
                return True
        return False

    def loadPlug(self, klass, params= {}) -> bool:
        if not self.isLoaded(klass):
            name = klass.__name__
            args = params.get(name, {})
            config = self.app.m_config.get(name, {})
            try:
                plug = klass(
                        app=self.app, 
                        config=config, 
                        **args)
                return plug
            except Exception as error:
                print("Error in plug loading: ", name, error)
                # raise

    def getPlugs(self, folder, modules=None):
        paths={}
        klasses=set()
        folder=str(folder)
        sys.path.insert(0, folder)
        modules=modules or os.listdir(folder)
        requirements=self.getRequirements(folder, modules)
        self.installRequirements(requirements)
        for name in modules:
            try:
                plug_path=os.path.join(folder, name)
                module = importlib.import_module(name)
                functor = getattr(module, "get_plug_class", None)
                if functor:
                    plugger = functor()
                    if type(plugger) != list:
                        plugger = [plugger]
                    for klass in plugger:
                        klasses.add(klass)
                        paths[klass]=plug_path
            except ModuleNotFoundError as error:
                msg = "Error in plug importing: "
                print(msg, name, error)
            except Exception as error:
                msg = "Error in plug importing: "
                print(msg, name, error)
                raise
        return klasses, paths

    def installRequirements(self, requirements):
        packages=self.getPackages()
        cmd=self.pip_command.split(' ')
        for req in requirements:
            if not req in packages:
                main(cmd+[req])

    def getRequirements(self, folder, modules):
        reqs = []
        for module in modules:
            path=os.path.join(folder, module)
            r = os.path.join(path, "requirements.txt")
            if os.path.exists(r):
                with open(r, "r") as f:
                    for i in f.readlines():
                        reqs += [i.strip("\n")]
        return set(reqs)

    def getPackages(self):
        packages=[]
        installed_packages = pkg_resources.working_set
        for i in installed_packages:
            packages+=[f"{i.key}"]
            packages+=[f"{i.key}=={i.version}"]
        return set(packages)

    def getPlug(self, name=None, path=None):
        if name:
            return self.plugs.get(name, None)
        elif path:
            return self.path_plugs.get(path, [])

    def delPlug(self, name=None, path=None):
        plug=self.getPlug(name=name, path=path)
        if plug:
            name=plug.__class__.__name__
            self.plugs.pop(name, None)
            pick=None
            for path, pick in self.path_plugs.items():
                if pick==plug: break
            if pick:
                self.path_plugs.pop(path, None)
