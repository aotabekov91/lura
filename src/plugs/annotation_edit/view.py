from PyQt6 import QtGui

from plug_qt import vimo

from plug_qt.widget import TableWidget

class EditorView(
        vimo.View, 
        TableWidget,
        ):

    def setFocus(self):
        super().setFocus()
        widget_data=self.widget('text')
        if widget_data:
            widget, _ = widget_data
            widget.setFocus()
            widget.setInputMode(True)

    # def setup(self):
    #     super().setup()
    #     # self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    #     self.hide()

    # def updatePosition(self):
    #     parent = self.parent()
    #     self.setGeometry(parent.geometry())
