from ..table import Table

class Part(Table):

    name='part'
    dname='part'
    fields=[
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'page int',
            'kind text',
            'text text',
            'summary text',
            'keyword text',
            'x1 real',
            'y1 real',
            'x2 real',
            'y2 real',
            'constraint unique_part unique (hash, page, kind, text, x1, y1, x2, y2)']
