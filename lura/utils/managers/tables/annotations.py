from .table import Table

class AnnotationsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'dhash str',
            'page int',
            'position text',
            'title text',
            'content text',
            'color text',
            'constraint unique_ann unique (dhash, page, position, color)'
        ]
        super().__init__(table='annotations', fields=self.fields)
