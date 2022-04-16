from lura.plugins.tables import Table 

class MetadataTable(Table):

    def __init__(self):

        self.fields=[
            'id integer PRIMARY KEY AUTOINCREMENT', 
            'author text',
            'title text',
            'url text',
            'journal text',
            'year int',
            'volume int',
            'number int',
            'edition int', 
            'pages text',
            'publisher text',
            'address text',
            'bibkey text',
            'kind text',
            'did int unique',
            'hash text',
            'type text',
            'createTime datetime',
            'accessTime datetime',
            'foreign key(did) references documents(id)'
            ]
        super().__init__(table='metadata', fields=self.fields)
