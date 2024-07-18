import os
import sys
import importlib
import typing as tp

from ..plug import Plug
from ..utils import dotdict

class Plugman(Plug):

    folder: str = "~"
    added: tp.Set[tp.Any]=set()
    autorun: tp.Set[tp.Any]=set()
    plugs: tp.Dict[tp.Any, tp.Any] = dotdict()

    def setup(self):
        super().setup()
        self.setFolder()

    def setFolder(self):
        self.folder = os.path.expanduser(self.folder)
        path=os.path.join(self.folder, 'autorun')
        autorun=self.app.createFolder(path)
        self.addAutorun(autorun)

    def addAutorun(self, folder):
        self.autorun.add(folder)

    def addPlugs(self, plugs=[]):
        self.added.update(plugs)

    def loadPlugs(self, params={}):
        plugs=self.added
        for folder in self.autorun:
            autorun_plugs=self.getAutoPlugs(folder)
            plugs.update(autorun_plugs)
        for plug in plugs: 
            self.loadPlug(plug, params)

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
                self.plugs[name] = plug
                return plug
            except Exception as e:
                print("Error in plug loading: ", name, e)
                raise

    def getAutoPlugs(self, folder):
        plugs=set()
        folder=str(folder)
        sys.path.insert(0, folder)
        for name in os.listdir(folder):
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
