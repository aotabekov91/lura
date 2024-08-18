from ..table import Table

class Pomodoro(Table):

    name='pomodoro'
    dname='pomodoro'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'task text',
        'task_id integer',
        'worked real not null',
        'timestamp timestamp not null',
        ]
