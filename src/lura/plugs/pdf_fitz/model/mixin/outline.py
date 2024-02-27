import fitz
from gizmo.ui.core import vimo
from gizmo.utils import Factory
from PyQt5 import QtCore, QtGui


class Outline:
    hasOutline = True

    def setup(self):
        super().setup()
        eklass = Factory(QtGui.QStandardItem, vimo.Element)
        mklass = Factory(QtGui.QStandardItemModel, vimo.Model)
        self.m_outline = mklass(
            name="outline",
            element_class=eklass,
        )
        self.m_outline.wantUniqView = True
        self.m_outline.wantView = ["OutlineView"]
        self.loaded.connect(self.setOutline)
        self.addModel("outline", self.m_outline)

    def outline(self):
        return self.m_outline

    def setOutline(self):
        o = self.m_data.outline
        r = self.m_outline.invisibleRootItem()
        self.loaded.disconnect(self.setOutline)
        self.loadOutline(o, r)

    def loadOutline(self, o, p):
        if not o:
            return
        t = o.title
        i = QtGui.QStandardItem(t)
        i.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        if o.dest.kind != fitz.LINK_NONE:
            # page = o.dest.ld.goTor.page + 1
            page = o.dest.page + 1
            i.setData(page)  # , QtCore.Qt.UserRole + 1)
            pi = i.clone()
            pi.setText(str(page))
            pi.setTextAlignment(QtCore.Qt.AlignRight)
            p.appendRow([i, pi])
        else:
            p.appendRow(i)
        if o.next != 0:
            self.loadOutline(o.next, p)
        if o.down != 0:
            self.loadOutline(o.down, i)
