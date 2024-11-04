from PyQt6 import QtCore
from plug_qt import vimo

class AnnotateSqliteModel(vimo.Model, QtCore.QObject):

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
        annotation_model=self.source()
        self.populateModel(annotation_model)
        add=getattr(annotation_model, 'elementAdded', None)
        rem=getattr(annotation_model, 'elementRemoved', None)
        upd=getattr(annotation_model, 'elementUpdated', None)
        if add: add.connect(self.addRow)
        if rem: rem.connect(self.removeRow)
        if upd: upd.connect(self.updateRow)

    def populateModel(self, source_model):
        rows=self.getRow({'source_id': self.source_id})
        annotator=self.app.plugman.plugs.get('Annotate')
        if rows and annotator:
            annotation_model=self.source()
            source_model=annotation_model.source()
            for row in rows: 
                self.parseMetadata(source_model, row)
                annotation_model.addAnnotate(data=row)

    def addRow(self, element):
        data=element.data()
        self.updateMetadata(data)
        idx=self.table.writeRow(data)
        data={self.uniq_field: idx}
        element.updateData(data)

    def removeRow(self, element):
        idx=element.data(self.uniq_field)
        data={self.uniq_field: idx} 
        self.table.removeRow(data)

    def updateRow(self, element, field=None):
        data=element.data()
        self.updateMetadata(data)
        data_copy=data.copy()
        criteria={self.uniq_field: data_copy[self.uniq_field]}
        if field: 
            data_copy={field: data_copy.get(field)}
        self.table.updateRow(criteria, data_copy) 

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
