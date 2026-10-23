import os
import sys
import importlib
import typing as tp
import pkg_resources

import tomli
from pip._internal.cli.main import main as pip_installer

from ..plug import Plug
from ..utils import dotdict

class Plugman(Plug):

    folder: str = "~"
    path_plugs={}
    pip_command=['install', '-q']
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
        aset, paths=self.getPlugs(folder, modules)
        aset=aset.union(set(self.added))
        self.loadKlasses(aset, paths, params)

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
                raise

    def getPlugs(self, folder, modules=None):
        paths={}
        klasses=set()
        folder=str(folder)
        modules=modules or os.listdir(folder)
        self.installModules(folder, modules)
        for data in modules:
            if type(data)==dict:
                data=data.get('folder', '')
            try:
                mfolder=os.path.join(folder, f'{data}/src')
                sys.path.insert(0, mfolder)
                plug_path=os.path.join(folder, data)
                module = importlib.import_module(data)
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
                print(msg, data, error)
                raise
            except Exception as error:
                msg = "Error in plug importing: "
                print(msg, data, error)
                raise
        return klasses, paths

    def installModules(self, folder, modules):
        requirements={}
        for data in modules:
            if type(data)==dict:
                data=data.get('folder', '')
            reqs=self.getRequirement(folder, data)
            requirements.update(reqs)
        self.installRequirements(requirements)

    def installRequirements(self, requirements):
        packages=self.getPackages()
        for name, package in requirements.items():
            name=name.replace('_', '-')
            if not name in packages:
                pip_installer(self.pip_command+[package])

    def getRequirement(self, folder, module):
        requirements = {} 
        path=os.path.join(folder, module)
        pyproj = os.path.join(path, "pyproject.toml")
        if os.path.exists(pyproj):
            with open(pyproj, 'rb') as f:
                pyproject=tomli.load(f)
                return pyproject.get('requirements', {})
        return requirements

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
