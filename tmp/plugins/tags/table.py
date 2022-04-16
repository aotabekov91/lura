from lura.plugins.tables import Table

class TaggedTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'tid int',
            'uid int',
            'kind text',
            'foreign key(tid) references tags(id)',
            'constraint unique_tagged unique (tid, uid, kind)',
        ]

        super().__init__(table='tagged', fields=self.fields)


class TagsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'tag text',
        ]
        super().__init__(table='tags', fields=self.fields)
