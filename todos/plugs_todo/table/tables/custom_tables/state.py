from ..table import Table

class State(Table):

    name='state'
    dname='state'
    uniq={'s_uniq': ('hash', 'kind', 'state')}
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'kind text',
        'state text',
        'value text',
        ]
