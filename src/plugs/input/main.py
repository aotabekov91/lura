from PyQt6 import QtCore
from plug import Plug, tag

from .nvim import NVim

class Input(Plug):

    deactivator=['<escape>', '<c-[>', '<c-q>']

    def setup(self):
        super().setup()
        self.m_agents={}
        self.setNVim()

    def setNVim(self):
        self.m_nvim=NVim(app=self.app)

    def nvim(self):
        return self.m_nvim

    def addAgent(self, action, kind, name):
        if not action in self.m_agents:
            self.m_agents[action]={}
        self.m_agents[action][kind]=name

    def getAgent(self, action, name=None, view=None):
        data=self.m_agents.get(action, {})
        if not name and view:
            name=view.__class__.__name__
        return data.get(name, None)

    def keyer(self, event):
        if event.type()==QtCore.QEvent.Type.KeyPress:
            mode=self.m_nvim.mode()
            pressed=self.app.earman.letters()
            if mode=='n' and pressed in self.deactivator: 
                self.octivateNVim()
            else:
                self.m_nvim.update(event.text())
            self.app.earman.clearKeys()
            return True
        return False

    def octivateNVim(self, **kwargs):
        self.m_nvim.setAgent()
        self.app.stateman.setKeyer()
        self.app.stateman.activate()

    @tag('e(edit)')
    def activateNVim(self, view=None, action='populate', mode='n', **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(action=action, view=view)
        if agent:
            self.m_nvim.setAgent(agent)
            self.app.stateman.setSubmode(mode)
            self.app.stateman.setKeyer(self.keyer)
            agent.activate(view=view, action=action, nvim=self.m_nvim, **kwargs)

    @tag(['<c-e>(normal/edit)', '<escape>/<c-[>(edit)'])
    def toggle(self):
        self.app.stateman.activate(mode='edit', toggle_mode=True)
