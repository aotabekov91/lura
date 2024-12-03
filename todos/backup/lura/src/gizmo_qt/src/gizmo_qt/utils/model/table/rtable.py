from .stable import STableModel


class RTableModel(STableModel):
    show_row = 0

    def load(self):
        rs = self.getTableRows()
        if self.show_row < len(rs):
            d = rs[self.show_row]
            self.m_data = d
            self.m_id = d.pop(self.uid)
            for k, v in self.widget_map.items():
                data = {"id": k.title(), k: d[k]}
                super().createElement(k, data)
            self.loaded.emit(self)

    def getWidgetMap(self, e):
        idx = e.index()
        return self.widget_map[idx]

    def updateTableRow(self, e):
        if self.table:
            idx = e.index()
            data = e.data()
            c = {self.uid: self.m_id}
            d = {idx: data[idx]}
            self.table.updateRow(c, d)
            return e
        return None

    def updateElement(self, e, data):
        if self.table:
            self.m_data.update(data)
            self.updateTableRow(e)
            self.elementUpdated.emit(e)
            return e
        return None
