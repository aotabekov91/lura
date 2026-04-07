import sys
import time

from PyQt6 import QtCore

from plug import Plug, tag

class General(Plug, QtCore.QObject):

    def delegate(self, action=None, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        self.app.delegman.delegate(
                mode='normal', view=view, action=action, data=kwargs)

    @tag(["<c-q>(any)", "(exec)"])
    def quit(self):
        self.app.appSoonQuits.emit()
        time.sleep(0.1)
        while self.app.wants_to_wait:
            time.sleep(0.01)
        sys.exit()

    @tag("(exec)")
    def save(self, path=None, **kwargs):
        self.delegate(action='save', path=path, **kwargs)

    @tag("(exec)")
    def open(self):
        pass

    @tag("(exec)")
    def help(self):
        pass

    # @tag('(exec)')
    # def help(self, command, **kwargs):
    #     path=self.m_data.get(command, None)
    #     if path:
    #         self.app.buffman.open(source=path)

    # def gatherMarkyFiles(self):
    #     plugs=self.app.plugman.plugs
    #     for name, plug in plugs.items(): 
    #         name=name.lower()
    #         file=plug.getFile('help.md')
    #         if file:
    #             self.m_data[name]=file
