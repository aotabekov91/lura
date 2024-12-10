import shlex
import argparse

from plug import Plug, tag

class Exec(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        self.setParser()

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
        print(text)
        self.toggle()
