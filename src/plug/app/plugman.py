import os
import sys
import importlib
import typing as tp

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
        self.plug_folder = self.app.createFolder(
            self.folder)

    def addPlugs(self, plugs=[]):
        self.added+=plugs

    def loadPlugs(self, params={}):
        plugs=self.getAutoPlugs(set())
        plugs=plugs.union(set(self.added))
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

    def getAutoPlugs(self, plugs=set()) -> tp.Set[tp.Any]:

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
