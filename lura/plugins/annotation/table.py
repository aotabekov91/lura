from lura.plugins.tables import Table

class AnnotationsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'did int',
            'page int',
            'position text',
            'title text',
            'content text',
            'quote text',
            'color text',
            'function text',
            'foreign key(did) references documents(id)',
            'constraint unique_ann unique (did, page, position)'
        ]
        super().__init__(table='annotations', fields=self.fields)
