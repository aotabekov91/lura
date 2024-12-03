from ..table import Table

class Annotation(Table):

    name='annotation'
    dname='annotation'
    uniq={
          'auniq': ('hash', 'kind', 'position', 'akind', 'function'),
         }
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'text text',
        'akind text',
        'content text',
        'position text',
        'function text',
        'kind text not null',
        ]
