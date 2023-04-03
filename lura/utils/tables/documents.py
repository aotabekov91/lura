from .table import Table

class DocumentsTable(Table):

    def __init__(self):

        self.lib = '/home/adam/docs/docs/'
        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'loc text unique',
            'hash text unique',
        ]
        super().__init__(table='documents', fields=self.fields)
