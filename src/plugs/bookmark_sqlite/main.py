from PyQt6 import QtCore

from plug import Plug

from .model import Model

class BookmarkSQLiteTable(Plug, QtCore.QObject):

    table_name='bookmark' 
    database_name='bookmark'
    fields = [
        'text text',
        'position text',
        'source_id text',
        'id integer PRIMARY KEY AUTOINCREMENT',
        ]
    uniq={'uniq_bookmark':  ('source_id', 'position')}

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
        bookmark=self.app.plugman.getPlug('Bookmark')
        table=self.app.plugman.getPlug('SQLiteTable')
        if bookmark and table:
            self.m_table=table.createTable(
                    uniq=self.uniq,
                    fields=self.fields,
                    table_name=self.table_name,
                    database_name=self.database_name)
            bookmark.modelCreated.connect(self.attachModel)

    def attachModel(self, model):
        if not model in self.m_models:
            source=model.source()
            source_id=source.id()
            table_model=Model(
                    source=model,
                    table=self.m_table, 
                    source_id=source_id)
            self.m_models[model]=table_model
