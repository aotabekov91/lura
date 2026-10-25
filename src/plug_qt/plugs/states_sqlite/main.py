from PyQt6 import QtCore

from plug import Plug

class StatesSQLiteTable(Plug, QtCore.QObject):

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
        self.table=None
        self.setParent(self.app.qapp)
        if self.app.running:
            self.addTable()
        else:
            self.app.appSoonStarts.connect(
                    self.addTable)

    def addTable(self):
        table=self.app.plugman.getPlug('SQLiteTable')
        if table:
            self.table=table.createTable(
                    uniq=self.uniq,
                    fields=self.fields,
                    table_name=self.table_name,
                    database_name=self.database_name)

    def getState(self, obj, state):
        criteria={'object': obj, 'state': state}
        return self.table.activate(
                action='getRow', criteria=criteria)

    def setState(self, obj, state, value):
        data={'object': obj, 'state': state, 'value': value}
        self.table.activate(
                action='writeRow', data=data)
