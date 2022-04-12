from lura.plugins.tables import Table

class PomodorosTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'task_id int',
            'start timestamp',
            'end  timestamp',
        ]
        super().__init__(table='pomodoro', fields=self.fields)

class PomodoroTasksTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'pomodoros int',
            'title text',
            'message text',
            'duration text',
            'pause text',
            'tags text',
        ]
        super().__init__(table='task', fields=self.fields)
