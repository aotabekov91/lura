import os

from lura.utils import Plugin

class Generic(Plugin):
    def __init__(self, app):
        super().__init__(app, name='generic')

    def exit(self):
        self.app.window.exit()

    def close(self):
        self.app.window.close()

    def toggleStatusBar(self):
        self.app.window.statusBar().toggle()
