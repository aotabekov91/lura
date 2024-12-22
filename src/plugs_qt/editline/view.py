from PyQt6 import QtCore, QtWidgets

from plug_qt import vimo

class EditlineView(vimo.View, QtWidgets.QWidget):

    textChanged = QtCore.pyqtSignal()
    editWanted = QtCore.pyqtSignal(bool)

    def __init__(
        self,
        *args,
        objectName="Editline",
        **kwargs,
    ):
        super().__init__(
            *args,
            objectName=objectName,
            **kwargs,
        )
        self.setupUI()

    def setupUI(self):
        l = QtWidgets.QHBoxLayout(self)
        self.m_label = QtWidgets.QLabel(
            ":", objectName="Mode"
        )
        self.m_text = QtWidgets.QLineEdit(objectName="Edit")
        self.m_text.textChanged.connect(self.textChanged)
        l.addWidget(self.m_label)
        l.addWidget(self.m_text)
        self.setContentsMargins(0, 0, 0, 0)
        l.setContentsMargins(0, 0, 0, 0)
        self.setLayout(l)
        l.setSpacing(0)

    def clear(self):
        self.m_text.clear()

    def text(self):
        return self.m_text.text()

    def setText(self, text):
        self.m_text.setText(text)

    def octivate(self, label=":", edit="", **kwargs):
        self.m_text.clear()
        self.m_text.hide()
        self.m_text.setText(str(edit))
        self.m_label.setText(str(label))
        self.editWanted.emit(False)
        super().octivate(**kwargs)

    def activate(
        self,
        label=":",
        edit="",
        keep=False,
        **kwargs,
    ):
        super().activate(**kwargs)
        self.show()
        self.m_text.show()
        self.m_text.setFocus()
        if not keep:
            self.m_text.setText(str(edit))
        self.m_label.setText(str(label))
        self.editWanted.emit(True)
