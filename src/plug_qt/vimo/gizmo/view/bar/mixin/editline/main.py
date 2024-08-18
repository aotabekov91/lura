from PyQt6 import QtCore

from .widget import EditlineWidget


class Editline:
    textChanged = QtCore.pyqtSignal()
    editWanted = QtCore.pyqtSignal(bool)

    def setupUI(self):
        super().setupUI()
        self.m_emit_activated=False
        self.setupEditline()

    def setupEditline(self):
        self.edit = EditlineWidget(objectName="Editline")
        self.edit.editWanted.connect(self.editWanted)
        self.edit.textChanged.connect(self.textChanged)
        self.edit.m_idx = self.stack.addWidget(self.edit)

    def clearEdit(self):
        self.edit.clearEdit()

    def toggleEdit(self):
        if self.m_emit_activated:
            self.octivateEdit()
        else:
            self.activateEdit()

    def octivateEdit(self, *args, **kwargs):
        self.m_emit_activated=False
        self.stack.setCurrentIndex(self.tabline.m_idx)
        return self.edit.octivateEdit(*args, **kwargs)

    def activateEdit(self, *args, **kwargs):
        self.m_emit_activated=True
        self.stack.setCurrentIndex(self.edit.m_idx)
        return self.edit.activateEdit(*args, **kwargs)

    def text(self):
        return self.edit.text()
