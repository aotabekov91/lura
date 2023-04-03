from lura.plugins.tables import Table

class BookmarksTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'did int',
            'page int',
            'text text',
            'position text',
            'foreign key(did) references documents(id)',
            'constraint unique_ann unique (did, page, position)'
        ]
        super().__init__(table='bookmarks', fields=self.fields)
