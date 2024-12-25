from PyQt6 import QtCore

from plug import Plug

from .view import EditlineView

class Editline(Plug, QtCore.QObject):

    textChanged = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.m_previous=None
        self.m_activated=False
        self.m_state=(None, None)
        self.setupEditline()

    def setupEditline(self):
        bar=self.app.view.bar
        self.edit = EditlineView(
                app=self.app,
                objectName="Editline",
                )
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
        self.edit.octivate(*args, **kwargs)
        bar_vis, stack_vis=self.m_state
        if not bar_vis:
            bar.octivate()
        if not stack_vis:
            bar.stack.hide()
        self.m_state=(None, None)

    def activate(self, *args, **kwargs):
        self.m_activated=True
        bar=self.app.view.bar
        self.m_previous=bar.stack.currentIndex()
        bar.stack.setCurrentIndex(self.edit.m_idx)
        self.m_state=bar.isVisible(), bar.stack.isVisible()
        bar.activate()
        bar.stack.show()
        self.edit.activate(*args, **kwargs)

    def text(self):
        return self.edit.text()
