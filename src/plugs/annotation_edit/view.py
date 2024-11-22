from PyQt6 import QtCore, QtGui

from plug_qt import vimo

from plug_qt.widget import TableWidget

class EditorView(
        vimo.View, 
        TableWidget,
        ):

    def event(self, event):
        if event.type()== QtCore.QEvent.Type.FocusOut:
            self.octivate()
        return super().event(event)


    # def setFocus(self):
    #     super().setFocus()
    #     widget_data=self.widget('text')
    #     if widget_data:
    #         widget, _ = widget_data
    #         widget.setFocus()
    #         widget.setInputMode(True)
