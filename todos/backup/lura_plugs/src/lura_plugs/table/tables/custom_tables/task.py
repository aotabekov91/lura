from ..table import Table

class Task(Table):

    name='task'
    dname='task'
    fields = [
    'id integer PRIMARY KEY AUTOINCREMENT',
    'status text default "pending" not null',
    'task text not null',
    'date datetime',
    'duration int',
    ]
