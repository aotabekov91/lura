from PyQt6 import QtCore

from plug_qt.gizmo import ItemListView

class ListView(ItemListView):

    def sizeHint(self):
        hint = super().sizeHint()
        if self.m_model:
            width=0
            height=0
            count = self.m_model.rowCount()
            for row in range(count):
                idx=self.m_model.index(row, 0)
                row_hint=self.sizeHintForIndex(idx)
                width=max(width, row_hint.width()) 
                height+=row_hint.height()
            hint=QtCore.QSize(width+5, height+5)
        return hint
