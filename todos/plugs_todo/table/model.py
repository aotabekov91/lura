from PyQt5 import QtCore
from gizmo.ui.qt.vimo import model

class Model(
        model.Model,
        QtCore.QObject,
        ):

    props=[]
    def setup(self):

        super().setup()
        self.setParent(self.app.qapp)
        self.uid=self.m_config.get(
                'uid', 'id')
        self.table=self.m_kwargs.get(
                'table')
        self.row_model=self.m_config.get(
                'row_model', False)
        self.autocreate=self.m_config.get(
                'autocreate', False)
        self.want=self.m_config.get(
                'want', False)

    def handleModel(self, m):

        if self.want=='attach':
            self.attachModel(m)
        elif self.want=='set':
            self.setModel(m)

    def setModel(self, m):

        if self.props:
            if not self.checkProp(self.props, m): 
                return
        if m.name!=self.name: return
        rows=self.getAllRows()
        for r in rows: m.createElement(r)
        add=getattr(m, 'elementAdded', None)
        rem=getattr(m, 'elementRemoved', None)
        upd=getattr(m, 'elementUpdated', None)
        if add: add.connect(self.addRow)
        if rem: rem.connect(self.removeRow)
        if upd: upd.connect(self.updateRow)

    def attachModel(self, m):
        
        if not self.checkProp(self.props, m): 
            return
        prop=f'hasTable{self.name}'
        if self.checkProp(prop, m): 
            return
        m.setProp(prop)
        idx=m.getLocator(kind='uniq', agent='model')
        if type(idx)==list:
            rows=[]
            for i in idx:
                rows+=self.getRows(i)
        else:
            rows=self.getRows(idx)
        qm=m.submodel(self.name)
        if self.row_model and rows:
            data=rows[0]
            for k, v in data.items():
                i=idx.copy()
                d={
                  'value':v, 
                  'field':k, 
                  'id': data[self.uid]
                  }
                d.update(i)
                qm.createElement(d)
        elif rows:
            for r in rows: 
                qm.createElement(r)
        add=getattr(qm, 'elementAdded', None)
        rem=getattr(qm, 'elementRemoved', None)
        upd=getattr(qm, 'elementUpdated', None)
        if add: add.connect(self.addRow)
        if rem: rem.connect(self.removeRow)
        if upd: upd.connect(self.updateRow)

    def addRow(self, e):

        d=e.data()
        idx=self.table.writeRow(d)
        data={self.uid: idx}
        e.updateData(data)

    def removeRow(self, e):

        idx=e.data(self.uid)
        d={self.uid: idx} 
        self.table.removeRow(d)

    def updateRow(self, e, fld=None):

        d=e.data().copy()
        c={self.uid: d[self.uid]}
        if fld: d={fld: d.get(fld)}
        self.table.updateRow(c, d) 

    def getAllRows(self):
        return self.table.getRows()

    def getRows(self, idx):

        rows=[]
        if self.table:
            rows=self.table.getRow(idx)
            if rows: return rows
            if not self.autocreate: return rows
            data={self.uid: idx}
            idx=self.table.writeRow(data)
            if idx: return self.getRows(idx)
        return rows

    def getRow(self, data):

        if self.table:
            return self.table.getRow(data)
        return []
