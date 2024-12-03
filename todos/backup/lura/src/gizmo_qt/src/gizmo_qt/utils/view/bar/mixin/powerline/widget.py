from PyQt6 import QtCore, QtWidgets


class PowerlineWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(objectName="Powerline")
        self.setupUI()

    def setupUI(self):
        self.mode = QtWidgets.QLabel(objectName="ModeName")
        self.submode = QtWidgets.QLabel(
            objectName="SubmodeName"
        )
        self.info = QtWidgets.QLabel(objectName="InfoName")
        self.detail = QtWidgets.QLabel(
            objectName="DetailName"
        )
        self.keys = QtWidgets.QLabel(objectName="KeysName")
        self.type = QtWidgets.QLabel(objectName="TypeName")
        self.model = QtWidgets.QLabel(
            objectName="ModelName"
        )
        self.view = QtWidgets.QLabel(objectName="ViewName")
        self.index = QtWidgets.QLabel(
            objectName="IndexName"
        )
        self.mode.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.submode.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.type.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.info.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.detail.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.view.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.keys.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.index.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        l = QtWidgets.QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)
        l.addWidget(self.mode)
        l.addWidget(self.submode)
        l.addWidget(self.info)
        l.addWidget(self.type)
        l.addWidget(self.detail)
        l.addStretch(100)
        ar = QtCore.Qt.AlignmentFlag.AlignRight
        l.addWidget(self.keys, ar)
        l.addWidget(self.model, ar)
        l.addWidget(self.view, ar)
        l.addWidget(self.index)
        self.setLayout(l)
        self.mode.hide()
        self.info.hide()
        self.view.hide()
        self.keys.hide()
        self.type.hide()
        self.model.hide()
        self.index.hide()
        self.detail.hide()
        self.submode.hide()

    def setText(self, kind, text):
        f = getattr(self, kind, None)
        if f:
            f.setText(str(text))
            if text is None:
                return f.hide()
            return f.show()
