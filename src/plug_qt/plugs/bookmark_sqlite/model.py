import json
from PyQt6 import QtCore

from plug_qt import vimo

class BookmarkSqliteModel(vimo.Model, QtCore.QObject):

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

    def attachSource(self, kind='connect'):
        self.populateModel()
        self.connectTable(kind='connect')
        if self.table:
            self.table.tableChanged.connect(self.updateModel)

    def updateModel(self, data):
        bmodel=self.source()
        if bmodel:
            action=data.get('action')
            self.connectTable('disconnect')
            kwargs=data.get('kwargs', {})
            source_model=bmodel.source()
            row=kwargs.get('data', {})
            if action=='writeRow':
                idx=data.get('result', None)
                self.parseMetadata(row)
                if not idx is None:
                    row[self.uniq_field]=idx
                    bmodel.add(data=row)
            elif action=='removeRow':
                criteria=kwargs.get('criteria', {})
                idx=criteria.get('id', None)
                element=bmodel.getElement(idx, by='id')
                bmodel.remove(element, data=row, by='id')
            self.connectTable('connect')

    def connectTable(self, kind):
        amodel=self.source()
        add=getattr(amodel, 'elementAdded', None)
        rem=getattr(amodel, 'elementRemoved', None)
        upd=getattr(amodel, 'elementUpdated', None)
        if kind=='connect':
            if add: add.connect(self.addRow)
            if rem: rem.connect(self.removeRow)
            if upd: upd.connect(self.updateRow)
        elif kind=='disconnect':
            if add: add.disconnect(self.addRow)
            if rem: rem.disconnect(self.removeRow)
            if upd: upd.disconnect(self.updateRow)

    def populateModel(self):
        rows=self.getRow(criteria={'source_id': self.source_id})
        if rows:
            model=self.source()
            for row in rows: 
                self.parseMetadata(row)
                model.createElement(row)

    def parseMetadata(self, data):
        metadata=data.get('metadata', None)
        if not metadata is None:
            metadata=metadata.replace("'", '"')
            try:
                data['position']=json.loads(metadata)
            except:
                data['position']=None

    def encodeMetadata(self, data):
        position=data.get('position', None)
        if position:
            data['metadata']=json.dumps(position)

    def addRow(self, element):
        data=element.data()
        self.encodeMetadata(data)
        idx=self.table.activate(action='writeRow', data=data)
        data={self.uniq_field: idx}
        element.updateData(data)

    def removeRow(self, element):
        idx=element.data(self.uniq_field)
        data={self.uniq_field: idx} 
        self.table.activate(action='removeRow', criteria=data)

    def updateRow(self, element, field=None):
        data=element.data().copy()
        criteria={self.uniq_field: data[self.uniq_field]}
        if field: 
            data={field: data.get(field)}
        self.encodeMetadata(data)
        self.table.activate(action='updateRow', criteria=criteria, data=data) 

    def getAllRows(self):
        return self.table.activate(action='getRows')

    def getRows(self, idx):
        rows=[]
        if self.table:
            rows=self.table.getRow(idx)
            if rows: return rows
            if not self.autocreate: 
                return rows
            data={self.uniq_field: idx}
            idx=self.table.activate(action='writeRow', data=data)
            if idx: 
                return self.getRows(idx)
        return rows

    def getRow(self, criteria):
        if self.table:
            return self.table.activate(action='getRow', criteria=criteria)
        return []
