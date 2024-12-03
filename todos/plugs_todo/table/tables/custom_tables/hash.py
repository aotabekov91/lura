from ..table import Table

class Hash(Table):

    name='hash'
    dname='hash'
    uniq={'uniq_h':  ('hash', 'path', 'kind')}
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'path text',
        'kind text',
        ]
