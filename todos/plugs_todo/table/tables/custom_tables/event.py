from ..table import Table

class Event(Table):

    name='event'
    dname='event'
    fields = [
    'id integer PRIMARY KEY AUTOINCREMENT',
    'description text',
    'supevent integer',
    'start datetime',
    'end datetime',
    'place text',
    'event text', 
    ]
