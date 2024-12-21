import inspect
import argparse
from collections import OrderedDict

from plug import Plug, tag

from PyQt6 import QtGui

from .model import Model, ListView

class Exec(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        self.m_model=Model()
        self.setParser()
        if self.app.running:
            self.gatherCommands()
        else:
            self.app.appSoonStarts.connect(
                    self.gatherCommands)

    def setupView(self):
        # self.m_view=self.app.buffman.createView(
        #         ListView,
        #         app=self.app,
        #         name='ExecView',
        #         attributes=[
        #                 {
        #                 'key': 'position', 
        #                 'value': {'ExecView': 'D|L'},
        #                 },])
        self.m_view=ListView()
        self.m_view.setModel(self.m_model)
        self.m_model.rowsRemoved.connect(self.updateView)
        self.m_model.rowsInserted.connect(self.updateView)

    def updateView(self):
        # self.m_view.first()
        # idx=self.m_view.currentIndex()
        # self.m_view.expand(idx)
        print(self.m_view.currentIndex())

    def gatherCommands(self):
        keys=self.app.earman.keys()
        objects=self.app.earman.objects()
        state=('exec', 'any', 'any', 'any')
        exec_keys=self.app.earman.getStateKeys(
                state, keys)
        commands=exec_keys['']
        func_data={}
        for oname, fname in commands:
            objs=objects.get(oname, [])
            for obj in objs:
                func=getattr(obj, fname, None)
                if func:
                    signiture = inspect.signature(func)
                    parser, data=self.getParser(signiture)
                    self.m_agents[fname]=(func, parser)
                    func_data[fname]=data
        self.m_model.populateModel(func_data)
        self.updateModel()
        self.setupView()

    def getParser(self, signiture):
        data=OrderedDict()
        prmts=signiture.parameters
        parser=argparse.ArgumentParser()
        for (name, prmt) in prmts.items():
            if name in ['args', 'kwargs']:
                continue
            if prmt.default==inspect.Parameter.empty:
                parser.add_argument(name)
                data[name]=[]
            else:
                data[name]=[prmt.default]
                parser.add_argument(name, default=prmt.default)
        return parser, data

    @tag('(exec)')
    def test(self, arg1, arg2='new'):
        pass

    @tag('<return>(exec)')
    def act(self):
        pass

    @tag('<c-j>(exec)')
    def down(self, xrange=[1]):
        self.m_view.goTo(kind='down', xrange=xrange)

    @tag('<c-k>(exec)')
    def up(self, xrange=[1]):
        self.m_view.goTo(kind='up', xrange=xrange)

    @tag('<c-l>(exec)')
    def right(self, xrange=[1]):
        self.m_view.goTo(kind='right', xrange=xrange)

    @tag('<c-h>(exec)')
    def left(self, xrange=[1]):
        self.m_view.goTo(kind='left', xrange=xrange)

    def connectEditline(self, kind='connect'):
        edit=self.app.plugman.getPlug('Editline')
        if edit and kind=='connect':
            edit.textChanged.connect(self.updateModel)
        elif edit and kind=='disconnect':
            edit.textChanged.disconnect(self.updateModel)

    def updateModel(self):
        edit=self.app.plugman.getPlug('Editline')
        text=edit.text()
        self.m_model.applyFilter(text)

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
        self.m_completer=Completer()
        self.m_completer.setModel(model)

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
            self.m_view.show()
            editline.toggle()
            mode=self.app.stateman.activate(
                    mode='exec', toggle_mode=True)

            if mode=='exec':
                self.connectEditline('connect')
                self.app.stateman.setPassive(
                        passive=['exec', 'any'])
            else:
                self.connectEditline('disconnect')
                self.app.stateman.setPassive()

    @tag('<tab>(exec)')
    def select(self):
        completion=self.m_completer.currentCompletion()
        if completion:
            editline=self.app.plugman.getPlug('Editline')
            editline.edit.setText(f'{completion} ')

    # @tag('<return>(exec)')
    # def act(self, command=None):
    #     if not command:
    #         edit=self.app.plugman.getPlug('Editline')
    #         command=edit.text()
    #     command = shlex.split(command)
    #     data=self.m_agents.get(command[0], None)
    #     self.toggle()
    #     if data:
    #         func, parser=data
    #         if parser:
    #             args=parser.parse_args(command[1:])
    #             args_dict=vars(args)
    #             func(**args_dict)
    #         else:
    #             func()
