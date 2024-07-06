import fitz
import gizmo
from app.utils import Factory
from PyQt6 import QtCore, QtGui


class Outline:
    hasOutline = True

    def setup(self):
        super().setup()
        eklass = Factory(QtGui.QStandardItem, gizmo.Element)
        mklass = Factory(QtGui.QStandardItemModel, gizmo.Model)
        self.m_outline = mklass(
            name="outline",
            element_class=eklass,
        )
        self.loaded.connect(self.setOutline)
        self.addModel("outline", self.m_outline)

    def outline(self):
        return self.m_outline

    def setOutline(self):
        o = self.m_data.outline
        r = self.m_outline.invisibleRootItem()
        self.loaded.disconnect(self.setOutline)
        try:
            self.loadOutline(o, r)
        except:
            pass

    def loadOutline(self, o, p):
        if not o:
            return
        t = o.title
        i = QtGui.QStandardItem(t)
        i.setFlags(
                QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        destination=o.destination(self.m_data)
        if destination!= fitz.LINK_NONE:
            page = destination.page + 1
            i.setData(page)  # , QtCore.Qt.UserRole + 1)
            pi = i.clone()
            pi.setText(str(page))
            pi.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            p.appendRow([i, pi])
        else:
            p.appendRow(i)
        if o.next != 0:
            self.loadOutline(o.next, p)
        if o.down != 0:
            self.loadOutline(o.down, i)
