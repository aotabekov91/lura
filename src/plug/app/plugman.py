import os
import sys
import pip
import importlib
import typing as tp
import pkg_resources

from ..plug import Plug
from ..utils import dotdict

class Plugman(Plug):

    folder: str = "~"
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
        plugs=self.getPlugs(folder, modules)
        plugs=plugs.union(set(self.added))
        for plug in plugs: 
            self.loadPlug(plug, params)

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
                self.plugs[name] = plug
                return plug
            except Exception as error:
                print("Error in plug loading: ", name, error)
                raise

    def getPlugs(self, folder, modules=None):
        plugs=set()
        folder=str(folder)
        sys.path.insert(0, folder)
        modules=modules or os.listdir(folder)
        requirements=self.getRequirements(folder, modules)
        self.installRequirements(requirements)
        for name in modules:
            try:
                plug_path=os.path.join(folder, name)
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

    def getPlug(self, name):
        return self.plugs.get(name)

    def installRequirements(self, requirements):
        packages=self.getPackages()
        for req in requirements:
            if not req in packages:
                pip.main(['install', req])

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
