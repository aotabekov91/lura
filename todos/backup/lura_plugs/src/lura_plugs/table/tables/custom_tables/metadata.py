from ..table import Table

class Metadata(Table):

    name='metadata' 
    dname='metadata'
    fields=[
        'id integer PRIMARY KEY AUTOINCREMENT', 
        'kind text',
        'hash text unique',
        'bibkey text unique',
        'author text',
        'url text',
        'title text',
        'journal text',
        'publisher text',
        'year int',
        'booktitle text',
        'institution text',
        'volume int',
        'number int',
        'edition int', 
        'pages text',
        'address text' ]
