from PyQt6 import QtCore

from plug import Plug

class StatesTable(Plug, QtCore.QObject):

    table_name='state' 
    database_name='state'
    fields = [
        'object text',
        'state text',
        'value text',
        'id integer PRIMARY KEY AUTOINCREMENT',
        ]
    uniq={'uniq_state':  ('object', 'state')}

    def setup(self):
        super().setup()
        self.m_table=None
        self.setParent(self.app.qapp)
        if self.app.running:
            self.addTable()
        else:
            self.app.appSoonStarts.connect(
                    self.addTable)

    def addTable(self):
        table=self.app.plugman.plugs.get('SQLiteTable')
        if table:
            self.m_table=table.createTable(
                    uniq=self.uniq,
                    fields=self.fields,
                    table_name=self.table_name,
                    database_name=self.database_name)

    def getState(self, obj, state):
        query={'object': obj, 'state': state}
        return self.m_table.getRow(query)

    def setState(self, obj, state, value):
        data={'object': obj, 'state': state, 'value': value}
        self.m_table.writeRow(data)
