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
