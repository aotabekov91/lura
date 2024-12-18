import shlex
import inspect
import argparse

from plug import Plug, tag

from PyQt6 import QtWidgets, QtGui

class Exec(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        self.setParser()
        if self.app.running:
            self.gatherCommands()
        else:
            self.app.appSoonStarts.connect(
                    self.gatherCommands)

    def gatherCommands(self):
        keys=self.app.earman.keys()
        objects=self.app.earman.objects()
        state=('exec', 'any', 'any', 'any')
        exec_keys=self.app.earman.getStateKeys(
                state, keys)
        commands=exec_keys['']
        for oname, fname in commands:
            objs=objects.get(oname, [])
            for obj in objs:
                func=getattr(obj, fname, None)
                if func:
                    signiture = inspect.signature(func)
                    parser=self.getParser(signiture)
                    self.m_agents[fname]=(func, parser)
        self.setCompleter()

    def setCompleter(self):
        model=QtGui.QStandardItemModel()
        for func in self.m_agents.keys():
            item=QtGui.QStandardItem(func)
            model.appendRow(item)
            if func=='installPicks':
                i=QtGui.QStandardItem('installPicks text 1')
                ii=QtGui.QStandardItem('installPicks text 2')
                item.appendRow(i)
                item.appendRow(ii)
        self.m_completer=QtWidgets.QCompleter()
        self.m_completer.setModel(model)
        self.m_completer.splitPath=self.splitPath

    def splitPath(self, path):
        return path.split(' ')

    def getParser(self, signiture):
        prmts=signiture.parameters
        if prmts:
            parser=argparse.ArgumentParser()
            for (name, prmt) in prmts.items():
                if name in ['kwargs']:
                    continue
                if prmt.default==inspect.Parameter.empty:
                    parser.add_argument(name)
                else:
                    parser.add_argument(name, default=prmt.default)
            return parser

    def setParser(self):
        self.m_parser=argparse.ArgumentParser()
        self.m_parser.add_argument('command')

    def addAgent(self, name, data):
        self.m_agents[name]=data

    def getAgent(self, name):
        return self.m_agents.get(name, {})

    @tag([":(normal)", "<escape>/<c-[>(exec)"])
    def toggle(self):
        editline=self.app.plugman.getPlug('Editline')
        if editline:
            editline.toggle()
            mode=self.app.stateman.activate(
                    mode='exec', toggle_mode=True)
            if mode=='exec':
                editline.edit.m_text.setCompleter(self.m_completer)
            else:
                editline.edit.m_text.setCompleter(None)

    @tag('<tab>(exec)')
    def select(self):
        completion=self.m_completer.currentCompletion()
        if completion:
            editline=self.app.plugman.getPlug('Editline')
            editline.edit.setText(f'{completion} ')

    @tag('<return>(exec)')
    def act(self, command=None):
        if not command:
            edit=self.app.plugman.getPlug('Editline')
            command=edit.text()
        command = shlex.split(command)
        data=self.m_agents.get(command[0], None)
        self.toggle()
        if data:
            func, parser=data
            if parser:
                args=parser.parse_args(command[1:])
                args_dict=vars(args)
                func(**args_dict)
            else:
                func()
