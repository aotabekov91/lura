from ..table import Table

class Autosave(Table):

    name='autosave'
    dname='autosave'
    uniq={'s_uniq': ('hash', 'kind', 'state')}
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text unique',
        'kind text',
        'state text',
        'value text',
        ]
