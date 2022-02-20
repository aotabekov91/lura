from lura.plugins.tables import Table 

class QuickmarksTable(Table):

    def __init__(self):

        self.fields=[
            'id integer PRIMARY KEY AUTOINCREMENT', 
            'did int',
            'page int',
            'left real',
            'top real',
            'key text',
            'comment text',
            'foreign key(did) references documents(id)',
            'constraint unique_ann unique (did, page, left, top)'
            ]
        super().__init__(table='quickmarks', fields=self.fields)
