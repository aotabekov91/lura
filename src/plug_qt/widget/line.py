from PyQt6 import QtCore, QtWidgets

class LineEdit(QtWidgets.QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
