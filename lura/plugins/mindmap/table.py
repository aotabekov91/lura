from lura.plugins.tables import Table

class MapsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'title text',
            'content text',
        ]
        super().__init__(table='maps', fields=self.fields)
