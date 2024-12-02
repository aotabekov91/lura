from PyQt6 import QtCore

from plug import Plug

from .view import EditlineWidget

class Editline(Plug, QtCore.QObject):

    textChanged = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.m_previous=None
        self.m_activated=False
        self.setupEditline()

    def setupEditline(self):
        bar=self.app.view.bar
        self.edit = EditlineWidget(objectName="Editline")
        self.edit.textChanged.connect(self.textChanged)
        self.edit.m_idx = bar.stack.addWidget(self.edit)

    def clear(self):
        self.edit.clear()

    def toggle(self):
        if self.m_activated:
            self.octivate()
        else:
            self.activate()

    def octivate(self, *args, **kwargs):
        self.m_activated=False
        bar=self.app.view.bar
        bar.stack.setCurrentIndex(self.m_previous)
        return self.edit.octivate(*args, **kwargs)

    def activate(self, *args, **kwargs):
        self.m_activated=True
        bar=self.app.view.bar
        self.m_previous=bar.stack.currentIndex()
        bar.stack.setCurrentIndex(self.edit.m_idx)
        return self.edit.activate(*args, **kwargs)

    def text(self):
        return self.edit.text()
