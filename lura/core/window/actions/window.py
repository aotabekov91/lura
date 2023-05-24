import os

from lura.utils import Plugin

class Generic(Plugin):
    def __init__(self, app):
        super().__init__(app, name='generic')

    def set_shortcuts(self):
        super().set_shortcuts(parent_widget='window')

    def saveDocument(self):
        self.app.window.saveDocument()

    def close(self):
        self.app.window.close()

    def closeView(self):
        self.app.window.closeView()

    def focusLeftDoc(self):
        self.app.window.focusLeftDoc()

    def focusView(self):
        self.app.window.focusView()

    def focusUpView(self):
        raise

    def focusDownView(self):
        raise

    def toggleStatusBar(self):
        self.app.window.statusBar().toggle()
