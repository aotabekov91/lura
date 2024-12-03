from ..table import Table

class Bookmark(Table):

    name='bookmark' 
    dname='bookmark'
    uniq={'uniq_b':  ('hash', 'kind', 'position')}
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'text text',
        'position text',
        'kind text not null',
        ]
