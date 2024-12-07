import pynvim
from PyQt6 import QtCore
from tempfile import NamedTemporaryFile

from plug import Plug

class NVim(Plug, QtCore.QObject):

    mode_mapping={
            'n': 'normal', 
            'v': 'visual', 
            'i': 'insert',
            'V': 'lvisual',
            '': 'bvisual',
            }

    def setup(self):
        super().setup()
        self.m_idx = 0
        self.m_mode=None
        self.m_agent=None
        self.m_abort=False
        self.m_file = NamedTemporaryFile()
        self.nvim = pynvim.attach(
                "child",
                argv=[
                    "/bin/env", 
                    "nvim", 
                    "--embed", 
                    "--headless"
                    ])

    def setAgent(self, agent=None):
        self.m_idx=0
        self.m_mode=None
        self.m_abort=False
        self.m_agent=agent
        self.clear()
        self.updateMode()

    def update(self, key):
        self.keyPress(key)
        while self.isBlocked():
            self.app.qapp.processEvents()
            if self.m_abort:
                return
        if self.m_agent:
            self.m_agent.activate(
                    action='update', nvim=self)
        self.updateMode()

    def clear(self):
        self.setText("")
        self.keyPress("<escape>")

    def updateMode(self):
        mode = self.mode()
        if self.m_mode != mode:
            self.m_mode = mode
            mode=self.mode_mapping.get(mode, mode)
            self.app.stateman.setSubmode(mode)

    def setText(self, text):
        self.buffer()[:] = text.split("\n")

    def text(self):
        return "\n".join(self.buffer()[:])

    def buffer(self):
        return self.nvim.current.buffer

    def cursorPosition(self):
        return self.nvim.windows[0].cursor

    def cursorAnchor(self):
        return [
            self.nvim.eval('line("v")'),
            self.nvim.eval('col("v")'),
        ]

    def keyPress(self, key):
        self.m_idx += 1
        self.nvim.input(key)
        self.nvim.call(
            "writefile",
            [self.m_idx],
            self.m_file.name,
            async_=True,
        )

    def mode(self):
        return self.eval("mode()")

    def commandLine(self):
        return self.eval("getcmdline()")

    def commandLineType(self):
        return self.eval("getcmdtype()")

    def byte(self, row, col):
        cmd = "line2byte(" + str(row) + ")"
        return self.eval(cmd) + col - 1

    def eval(self, expr):
        return self.nvim.eval(expr)

    def isBlocked(self):
        with open(self.m_file.name, "r") as f:
            data = f.read().strip()
            return data != str(self.m_idx)
        return False
