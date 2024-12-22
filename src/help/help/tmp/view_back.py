from PyQt6 import QtWidgets

from plug_qt import vimo

class HelpView(vimo.View, QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs):
        super(vimo.View, self).__init__(*args, **kwargs)
        super(QtWidgets.QTextEdit, self).__init__()
