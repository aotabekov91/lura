from ..table import Table

class Quickmark(Table):

    name='quickmark'
    dname='quickmark'
    uniq={'quniq': ('hash', 'kind', 'mark')}
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'mark text',
        'position text',
        'kind text not null'
        ]
