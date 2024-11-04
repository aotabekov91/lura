from PyQt6 import QtCore

from plug import Plug

from .model import AnnotateSqliteModel

class AnnotateSqliteTable(Plug, QtCore.QObject):

    table_name='annotate' 
    database_name='annotate'
    fields = [
        'text text',
        'metadata text',
        'source_id text',
        'id integer PRIMARY KEY AUTOINCREMENT',
        ]
    uniq={'uniq_annotate':  ('source_id', 'metadata')}

    def table(self):
        return self.m_table

    def model(self, source):
        return self.m_models.get(source, None)

    def setup(self):
        super().setup()
        self.m_models={}
        self.m_table=None
        self.setParent(self.app.qapp)
        if self.app.running:
            self.addTable()
        else:
            self.app.appSoonStarts.connect(
                    self.addTable)

    def addTable(self):
        annotate=self.app.plugman.plugs.get('Annotate')
        table=self.app.plugman.plugs.get('SQLiteTable')
        if annotate and table:
            self.m_table=table.createTable(
                    uniq=self.uniq,
                    fields=self.fields,
                    table_name=self.table_name,
                    database_name=self.database_name)
            annotate.modelCreated.connect(self.attachModel)

    def attachModel(self, model):
        if not model in self.m_models:
            source=model.source()
            source_id=source.id()
            table_model=AnnotateSqliteModel(
                    source=model,
                    app=self.app,
                    table=self.m_table, 
                    source_id=source_id)
            self.m_models[model]=table_model
