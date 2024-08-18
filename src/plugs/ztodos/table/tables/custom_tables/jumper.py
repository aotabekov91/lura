from ..table import Table

class Jumper(Table):

    name='jumper'
    dname='jumper'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'url text',
        'page int',
        'position text',
        'constraint unique_hash_jump unique (hash, page, position)',
        'constraint unique_url_jump unique (url, page, position)' ]
