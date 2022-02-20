from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import PomodorosTable, PomodoroTasksTable

class DatabaseConnector(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent.window
        self.s_settings=settings
        self.setup()

    def setup(self):
        if self.s_settings is not None:
            self.window.plugin.tables.addTable(PomodorosTable)
            self.window.plugin.tables.addTable(PomodoroTasksTable)
            self.m_tasks=self.window.plugin.tables.pomodorotasks
            self.m_pomodoros=self.window.plugin.tables.pomodoros
        else:
            self.m_tasks=PomodoroTasksTable()
            self.m_pomodoros=PomodorosTable()

    def addTask(self, taskDict):
        self.m_tasks.writeRow(taskDict)

    def tasks(self):
        return self.m_tasks.getRow({'field':'tags', 'value':'regular'})

    def get(self, tid):
        return self.m_tasks.getRow({'field':'id', 'value':tid})[0]

    def getAllTasks(self):
        return self.m_tasks.getAll()

    def getAll(self):
        return self.m_pomodoros.getAll()

    def setTags(self, pid, tags):
        self.m_tasks.updateRow({'field':'id', 'value':pid}, {'tags':tags})

    def delete(self, pid):
        self.m_tasks.removeRow({'field':'id', 'value':pid})

    def addPomodoro(self, pomoDict):
        self.m_pomodoros.writeRow(pomoDict)

