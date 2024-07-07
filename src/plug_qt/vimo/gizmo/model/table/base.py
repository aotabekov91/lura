from PyQt6 import QtCore

from ...model import Model
from ...element import TableElement


class TableModel(Model):
    table = None
    wantUniqView = True
    element_class = TableElement
    elementAdded = QtCore.pyqtSignal(object)
    elementRemoved = QtCore.pyqtSignal(object)
    elementUpdated = QtCore.pyqtSignal(object)

    def setup(self):
        self.m_rows = {}
        super().setup()
        self.m_listwidget = None

    def attachBaseModel(self):
        bm = self.m_kwargs.get("base_model")
        if bm:
            self.setBasemodel(bm)
            bm.addModel(self.name, self)

    def listWidget(self):
        return self.m_listwidget

    def setListWidget(self, listwidget=None):
        self.m_listwidget = listwidget

    def getTableRows(self):
        rows = []
        if self.m_id and self.table:
            rows = self.table.getRow(self.m_id)
            autocreate = self.m_config.get(
                "autocreate", False
            )
            if rows:
                return rows
            if not autocreate:
                return rows
            self.addTableRow(self.id())
            self.m_config["autocreate"] = False
            return self.getTableRows()
        return rows

    def load(self):
        for r in self.getTableRows():
            self.createElement(r[self.uid], r)
        self.loaded.emit(self)
        self.attachBaseModel()

    def createElement(self, idx, data):
        e = self.element_class(
            data=data, index=idx, model=self
        )
        self.m_elements[idx] = e
        self.elementCreated.emit(e)
        return e

    def findElement(self, cond, by="id"):
        for e in self.m_elements.values():
            d = e.data()
            if cond == d.get(by, None):
                return e

    def getTableRow(self, data):
        if self.table:
            return self.table.getRow(data)
        return []

    def removeTableRow(self, e):
        if self.table:
            idx = e.index()
            d = {self.uid: idx}
            self.table.removeRow(d)
            return e
        return None

    def updateTableRow(self, e, fld=None):
        if self.table:
            idx = e.index()
            c = {self.uid: idx}
            d = e.data().copy()
            if fld:
                d = {fld: d.get(fld)}
            self.table.updateRow(c, d)
            return e
        return None

    def updateElement(self, e, data):
        if self.table:
            e.m_data.update(data)
            self.updateTableRow(e)
            self.elementUpdated.emit(e)
            return e
        return None

    def removeElement(self, e):
        self.removeTableRow(e)
        data = self.m_elements.pop(e.index())
        if data:
            self.elementRemoved.emit(e)
        return e

    def addTableRow(self, data):
        if self.table:
            idx = self.table.writeRow(data)
            rs = self.getTableRow({self.uid: idx})
            return rs[0]

    def addElement(self, data):
        r = self.addTableRow(data)
        idx = r[self.uid]
        e = self.element(idx)
        if e:
            e.updateData(r)
            self.elementUpdated.emit(e)
        else:
            e = self.createElement(idx, r)
            self.elementAdded.emit(e)
        e.m_data.update(data)
        return e
