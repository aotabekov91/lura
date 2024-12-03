from plug_qt import vimo

from plug_qt.gizmo import RowWidget

class EditorView(vimo.View, RowWidget):

    def activate(self, *args, **kwargs):
        self.app.stateman.viewChanged.connect(
                self.checkViewChange)
        super().activate(*args, **kwargs)

    def octivate(self, *args, **kwargs):
        self.app.stateman.viewChanged.disconnect(
                self.checkViewChange)
        super().octivate(*args, **kwargs)

    def checkViewChange(self, view):
        if self!=view:
            self.octivate()

    # def event(self, event):
    #     if event.type()== QtCore.QEvent.Type.FocusOut:
    #         self.octivate()
    #     return super().event(event)

    # def setFocus(self):
    #     super().setFocus()
    #     widget_data=self.widget('text')
    #     if widget_data:
    #         widget, _ = widget_data
    #         widget.setFocus()
    #         widget.setInputMode(True)
