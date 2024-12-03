from ..table import Table

class Leaf(Table):

    name='leaf'
    dname='tree'
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

class Tree(Table):

    name='tree'
    dname='tree'
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
