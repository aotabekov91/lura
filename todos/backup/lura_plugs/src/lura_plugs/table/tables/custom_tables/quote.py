from ..table import Table

class Quote(Table):

    name='quote'
    dname='quotes'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'author text',
        'text text',
        'constraint unique_quote unique (author, text)']
