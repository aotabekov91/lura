import json
from PyQt6 import QtCore

from plug_qt import vimo

class Model(vimo.Model, QtCore.QObject):

    def __init__(
            self,
            table=None,
            source_id=None,
            uniq_field='id',
            autocreate=False,
            **kwargs,
            ):
        super().__init__(**kwargs)
        self.table=table
        self.source_id=source_id
        self.autocreate=autocreate
        self.uniq_field=uniq_field
        self.attachSource()

    def attachSource(self):
        source=self.source()
        self.populateModel(source)
        add=getattr(source, 'elementAdded', None)
        rem=getattr(source, 'elementRemoved', None)
        upd=getattr(source, 'elementUpdated', None)
        if add: add.connect(self.addRow)
        if rem: rem.connect(self.removeRow)
        if upd: upd.connect(self.updateRow)

    def populateModel(self, model):
        rows=self.getRow({'source_id': self.source_id})
        for row in rows: 
            self.decodeMetadata(row)
            model.createElement(row)

    def decodeMetadata(self, data):
        metadata=data.get('metadata').replace("'", '"')
        if metadata:
            data['position']=json.loads(metadata)

    def encodeMetadata(self, data):
        position=data.get('position', None)
        if position:
            data['metadata']=json.dumps(position)

    def addRow(self, element):
        data=element.data()
        self.encodeMetadata(data)
        idx=self.table.writeRow(data)
        data={self.uniq_field: idx}
        element.updateData(data)

    def removeRow(self, element):
        idx=element.data(self.uniq_field)
        data={self.uniq_field: idx} 
        self.table.removeRow(data)

    def updateRow(self, element, field=None):
        data=element.data().copy()
        criteria={self.uniq_field: data[self.uniq_field]}
        if field: 
            data={field: data.get(field)}
        self.encodeMetadata(data)
        self.table.updateRow(criteria, data) 

    def getAllRows(self):
        return self.table.getRows()

    def getRows(self, idx):
        rows=[]
        if self.table:
            rows=self.table.getRow(idx)
            if rows: return rows
            if not self.autocreate: 
                return rows
            data={self.uniq_field: idx}
            idx=self.table.writeRow(data)
            if idx: 
                return self.getRows(idx)
        return rows

    def getRow(self, data):
        if self.table:
            return self.table.getRow(data)
        return []
