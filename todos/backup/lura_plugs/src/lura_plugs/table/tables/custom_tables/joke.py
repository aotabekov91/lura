from ..table import Table

class Joke(Table):

    name='joke'
    dname='jokes'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'author text',
        'name text',
        'text text',
        'constraint unique_quote unique (name, text)']
