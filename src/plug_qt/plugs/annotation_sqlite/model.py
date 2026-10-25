from PyQt6 import QtCore
from plug_qt import vimo

class AnnotationSQLiteModel(vimo.Model, QtCore.QObject):

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
        self.populateModel()
        self.connectTable(kind='connect')
        if self.table:
            self.table.tableChanged.connect(self.updateModel)

    def updateModel(self, data):
        annotation_model=self.source()
        if annotation_model:
            action=data.get('action')
            self.connectTable('disconnect')
            kwargs=data.get('kwargs', {})
            source_model=annotation_model.source()
            if action=='writeRow':
                row=kwargs.get('data', {})
                idx=data.get('result', None)
                self.parseMetadata(source_model, row)
                if not idx is None:
                    row[self.uniq_field]=idx
                    annotation_model.add(
                            model=source_model, data=row)
            elif action=='removeRow':
                criteria=kwargs.get('criteria', {})
                idx=criteria.get('id', None)
                element=annotation_model.getElement(
                        idx, by='id')
                annotation_model.remove(
                        model=source_model, annotation=element)
            self.connectTable('connect')

    def connectTable(self, kind='connect'):
        annotation_model=self.source()
        add=getattr(annotation_model, 'elementAdded', None)
        rem=getattr(annotation_model, 'elementRemoved', None)
        upd=getattr(annotation_model, 'elementUpdated', None)
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
        annotator=self.app.plugman.getPlug('Annotate')
        if rows and annotator:
            annotation_model=self.source()
            source_model=annotation_model.source()
            for row in rows: 
                self.parseMetadata(source_model, row)
                annotation_model.add(model=source_model, data=row)

    def addRow(self, element):
        data=element.data()
        self.updateMetadata(data)
        idx=self.table.activate(action='writeRow', data=data)
        data={self.uniq_field: idx}
        print(idx, data)
        element.updateData(data)

    def removeRow(self, element):
        idx=element.data(self.uniq_field)
        data={self.uniq_field: idx} 
        self.table.activate(action='removeRow', criteria=data)

    def updateRow(self, element, field=None):
        data=element.data()
        self.updateMetadata(data)
        data_copy=data.copy()
        criteria={self.uniq_field: data_copy[self.uniq_field]}
        if field: 
            data_copy={field: data_copy.get(field)}
        self.table.activate(
                action='updateRow', 
                criteria=criteria, 
                data=data_copy) 

    def getAllRows(self):
        return self.table.activate(action='getRows')

    def getRows(self, idx):
        rows=[]
        if self.table:
            rows=self.table.activate(action='getRow', criteria=idx)
            if rows: return rows
            if not self.autocreate: 
                return rows
            data={self.uniq_field: idx}
            idx=self.table.writeRow(data)
            if idx: 
                return self.getRows(idx)
        return rows

    def getRow(self, criteria):
        if self.table:
            return self.table.activate(
                    action='getRow', criteria=criteria)
        return []

    def updateMetadata(self, data):
        position=self.getPosition(data)
        kind=data.get("annotation_kind")
        color=data.get("annotation_color", '')
        color=':'.join([str(f) for f in color])
        data["metadata"] = f"{position}|{kind}|{color}"
        return data

    def parseMetadata(self, model, data):
        metadata=data.get('metadata')
        parts=metadata.split('|')
        page=int(parts[0])
        location=parts[1]
        locs=location.split('_')
        data['box']=[]
        for l in locs:
            corners=l.split(':')
            x=float(corners[0])
            y=float(corners[1])
            w=float(corners[2])
            h=float(corners[3])
            data['box']+=[QtCore.QRectF(x, y, w, h)]
        data['page']=page
        data['element']=model.element(page)
        data['annotation_kind']=parts[2]
        rgb_parts=parts[3].split(':')
        rgb=[float(c) for c in rgb_parts] 
        data['annotation_color']=rgb
        return data

    def getPage(self, data):
        element = data.get("element", None)
        if element:
            return element.index()
        item = data.get("item", None)
        if item:
            element = item.element()
            return element.index()

    def getPosition(self, data):
        text = []
        page = self.getPage(data)
        boxes = data.get("box", [])
        for box in boxes:
            x = str(box.x())[:6]
            y = str(box.y())[:6]
            w = str(box.width())[:6]
            h = str(box.height())[:6]
            text += [f"{x}:{y}:{w}:{h}"]
        loc = "_".join(text)
        return f"{page}|{loc}"
