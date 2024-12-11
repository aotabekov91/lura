import shlex
import inspect
import argparse

from plug import Plug, tag

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
        edit=self.app.plugman.getPlug('Editline')
        if edit:
            edit.toggle()
            self.app.stateman.activate(
                    mode='exec', toggle_mode=True)

    @tag('<return>(exec)')
    def activate(self):
        edit=self.app.plugman.getPlug('Editline')
        text=edit.text()
        text = shlex.split(text)
        data=self.m_agents.get(text[0], None)
        self.toggle()
        if data:
            func, parser=data
            if parser:
                args=parser.parse_args(text[1:])
                args_dict=vars(args)
                func(**args_dict)
            else:
                func()
