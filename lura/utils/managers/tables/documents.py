from .table import Table

class DocumentsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'path text',
        ]
        super().__init__(table='documents', fields=self.fields)
