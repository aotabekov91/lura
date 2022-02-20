import time

from enum import Enum
from datetime import datetime

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

from lura.plugins.pomodoro.graphs import Heatmap

from .connect import DatabaseConnector

class Mode(Enum):
    work = 1
    rest = 2


class Status(Enum):
    workFinished = 1
    restFinished = 2
    repetitionsReached = 3


class Pomodoro(QWidget):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.s_settings=settings
        self.location='right'
        self.name='pomodoro'

        self.globalKeys={
                'Ctrl+Shift+p': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):
        self.beginningStamp=None
        self.endStamp=None
        self.db=DatabaseConnector(self, self.s_settings)

        self.setupTrayicon()
        self.setupVariables()
        self.setupUi()
        self.setupConnections()

    def setupVariables(self):
        self.workEndTime = QTime(int(0), int(0), int(5))
        self.restEndTime = QTime(int(0), int(0), int(5))

        self.timeFormat = "hh:mm:ss"
        self.time = QTime(0, 0, 0, 0)
        self.workTime = QTime(0, 0, 0, 0)
        self.restTime = QTime(0, 0, 0, 0)
        self.totalTime = QTime(0, 0, 0, 0)
        self.currentMode = Mode.work
        self.maxRepetitions = -1
        self.currentRepetitions = 0

    def setupConnections(self):
        """ Create button connections """
        self.startButton.clicked.connect(self.startTimer)
        self.startButton.clicked.connect(lambda: self.startButton.setDisabled(True))
        self.startButton.clicked.connect(lambda: self.pauseButton.setDisabled(False))
        self.startButton.clicked.connect(lambda: self.resetButton.setDisabled(False))
        self.pauseButton.clicked.connect(self.pauseTimer)
        self.pauseButton.clicked.connect(lambda: self.startButton.setDisabled(False))
        self.pauseButton.clicked.connect(lambda: self.pauseButton.setDisabled(True))
        self.pauseButton.clicked.connect(lambda: self.resetButton.setDisabled(False))
        self.pauseButton.clicked.connect(lambda: self.startButton.setText("continue"))
        self.resetButton.clicked.connect(self.resetTimer)
        self.resetButton.clicked.connect(lambda: self.startButton.setDisabled(False))
        self.resetButton.clicked.connect(lambda: self.pauseButton.setDisabled(True))
        self.resetButton.clicked.connect(lambda: self.resetButton.setDisabled(True))
        self.resetButton.clicked.connect(lambda: self.startButton.setText("start"))

    def setupUi(self):
        self.size_policy = sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        self.setupTasks()
        self.insertTasks()
        if self.window is not None:
            self.window.setTabLocation(self, self.location, self.name) 
        self.activated=False
        self.taskInput.show()

    def toggle(self):
        if not self.activated:
            if self.window is not None: self.window.activateTabWidget(self)
            self.setFocus()
            self.show()
            self.activated=True
        else:
            if self.window is not None: self.window.deactivateTabWidget(self)
            self.activated=False

    def toggleGroup(self, group):
        if group.isVisible():
            group.hide()
        else:
            group.show()

    def setupTasks(self):

        """ Create vertical tasks container """
        self.tasksWidgetLayout = QVBoxLayout(self)

        toolbox=QWidget()
        toolbox.m_layout=QHBoxLayout(toolbox)
        self.tasksWidgetLayout.addWidget(toolbox)

        # Task input group
        self.taskInput=QGroupBox()
        layout=QFormLayout(self.taskInput)

        self.title=QLineEdit(self.taskInput)
        self.pomodoros=QLineEdit(self.taskInput)
        self.pomodoros.setText('4')
        self.workDuration=QLineEdit(self.taskInput)
        self.workDuration.setText('25m')
        self.pauseDuration=QLineEdit(self.taskInput)
        self.pauseDuration.setText('5m')
        self.message=QLineEdit(self.taskInput)

        layout.addRow('Title', self.title)
        layout.addRow('Duration', self.workDuration)
        layout.addRow('Pause', self.pauseDuration)
        layout.addRow('Pomodoros', self.pomodoros)
        layout.addRow('Message', self.message)

        controls=QWidget()
        controls.m_layout=QHBoxLayout(controls)


        startButton=QPushButton('Start', self.taskInput)
        startButton.clicked.connect(lambda: self.startTask(kind='new'))

        saveButton=QPushButton('Save', self.taskInput)
        saveButton.clicked.connect(self.saveTask)

        saveAndStartButton=QPushButton('Save and Start', self.taskInput)
        saveAndStartButton.clicked.connect(self.saveAndStartTask)

        controls.m_layout.addWidget(startButton)
        controls.m_layout.addWidget(saveButton)
        controls.m_layout.addWidget(saveAndStartButton)

        layout.addRow(controls)

        self.taskInputButton=QPushButton('New')
        self.taskInputButton.clicked.connect(lambda: self.toggleGroup(self.taskInput))
        toolbox.m_layout.addWidget(self.taskInputButton)
        self.tasksWidgetLayout.addWidget(self.taskInput)
        self.taskInput.hide()

        # Tasks group
        self.tasksBox=QGroupBox()
        layout=QVBoxLayout(self.tasksBox)
        self.taskModel=QStandardItemModel()
        self.taskList=QListView()
        self.taskList.setModel(self.taskModel)
        self.taskList.doubleClicked.connect(self.reset)

        controls=QWidget()
        controls.m_layout=QHBoxLayout(controls)

        startTask=QPushButton('Start', self.tasksBox)
        startTask.clicked.connect(lambda: self.startTask('list'))
        removeTask=QPushButton('Remove', self.tasksBox)
        removeTask.clicked.connect(self.removeTask)
        deleteTask=QPushButton('Delete', self.tasksBox)
        deleteTask.clicked.connect(self.deleteTask)

        controls.m_layout.addWidget(startTask)
        controls.m_layout.addWidget(removeTask)
        controls.m_layout.addWidget(deleteTask)

        layout.addWidget(self.taskList)
        layout.addWidget(controls)

        self.tasksButton=QPushButton('Tasks')
        self.tasksButton.clicked.connect(lambda: self.toggleGroup(self.tasksBox))
        toolbox.m_layout.addWidget(self.tasksButton)
        self.tasksWidgetLayout.addWidget(self.tasksBox)
        self.tasksBox.hide()

        """ Create timer groupbox"""
        # self.lcdDisplayGroupBox = QGroupBox("Time")
        self.lcdDisplayGroupBox = QGroupBox()
        self.lcdDisplayGroupBoxLayout = QVBoxLayout(self.lcdDisplayGroupBox)

        self.status=QWidget()
        self.status.setFixedHeight(40)
        self.taskLabel=QLabel('Task')
        self.pomodoroNumber=QLabel('0')

        layout=QHBoxLayout(self.status)
        layout.addWidget(self.taskLabel)
        layout.addStretch(1)
        layout.addWidget(self.pomodoroNumber)

        self.lcdDisplayGroupBoxLayout.addWidget(self.status)

        self.timeDisplay = QLCDNumber(8, sizePolicy=self.size_policy)
        self.timeDisplay.setFixedHeight(100)
        self.timeDisplay.display("00:00:00")
        self.lcdDisplayGroupBoxLayout.addWidget(self.timeDisplay)

        """ Create pause, start and reset buttons"""
        self.buttonContainer = QWidget()
        self.buttonContainer.setFixedHeight(40)
        self.buttonContainerLayout = QHBoxLayout(self.buttonContainer)
        self.startButton = self.makeButton("start", disabled=False)
        self.resetButton = self.makeButton("reset")
        self.pauseButton = self.makeButton("pause")
        """ Add widgets to container """
        self.buttonContainerLayout.addWidget(self.pauseButton)
        self.buttonContainerLayout.addWidget(self.startButton)
        self.buttonContainerLayout.addWidget(self.resetButton)

        self.lcdDisplayGroupBoxLayout.addWidget(self.buttonContainer)

        self.timerBoxButton=QPushButton('Timer')
        self.timerBoxButton.clicked.connect(lambda: self.toggleGroup(self.lcdDisplayGroupBox))
        toolbox.m_layout.addWidget(self.timerBoxButton)
        self.tasksWidgetLayout.addWidget(self.lcdDisplayGroupBox)
        self.lcdDisplayGroupBox.hide()

        # Report group
        self.reportBox=QGroupBox()
        layout=QVBoxLayout(self.reportBox)
        self.heatmap=Heatmap(self, self.db)
        # self.pie=PieChart(self)
        # self.heatmap.widgetDoubleClick.connect(self.pie.on_widgetDoubleClick)
        layout.addWidget(self.heatmap)
        # layout.addWidget(self.pie)

        self.reportButton=QPushButton('Report')
        self.reportButton.clicked.connect(lambda: self.toggleGroup(self.reportBox))
        toolbox.m_layout.addWidget(self.reportButton)
        self.tasksWidgetLayout.addWidget(self.reportBox)
        self.reportBox.hide()

        self.tasksWidgetLayout.addStretch(1)

        # Mode group
        self.modeComboBox = QComboBox()
        self.modeComboBox.addItems(["work", "rest"])
        self.modeComboBox.currentTextChanged.connect(self.updateCurrentMode)

    def submitPomodoro(self):
        if self.beginningStamp is None: return 
        self.endStamp=datetime.now()
        self.db.addPomodoro({'task_id':self.currentTaskId, 'start':self.beginningStamp, 'end':self.endStamp})
        self.currentTaskId=None
        self.beginningStamp=None
        self.endStamp=None

    def removeTask(self):
        index=self.taskList.currentIndex()
        if index is None: return 
        text=self.taskModel.itemFromIndex(index)
        self.db.setTags(text.m_id, '')
        self.insertTasks()

    def deleteTask(self):
        index=self.taskList.currentIndex()
        if index is None: return 
        text=self.taskModel.itemFromIndex(index)
        self.db.delete(text.m_id)
        self.insertTasks()

    def getData(self):
        return {'title': self.title.text(),
                'pomodoros': int(self.pomodoros.text()),
                'duration': self.workDuration.text(),
                'pause': self.pauseDuration.text(),
                'message': self.message.text(),
                }

    def getTask(self, kind):
        if kind== 'list': return self.reset()
        if kind == 'new': 
            data=self.getData()
            self.db.addTask(data)
            self.currentTaskId=self.db.getAllTasks()[-1]['id']
            return data


    def saveAndStartTask(self):
        self.saveTask()
        self.startTask(kind='new')

    def startTask(self, kind):
        self.taskInput.hide()
        self.tasksBox.hide()
        self.lcdDisplayGroupBox.show()
        self.setTask(self.getTask(kind))

        self.startTimer()
        self.startButton.setDisabled(True)
        self.pauseButton.setDisabled(False)
        self.resetButton.setDisabled(False)

    def reset(self, index=None):
        if index is None: index=self.taskList.currentIndex()
        text=self.taskModel.itemFromIndex(index)
        task=self.db.get(text.m_id)

        self.currentTaskId=text.m_id
        self.title.setText(task['title'])
        self.pomodoros.setText(str(task['pomodoros']))
        self.workDuration.setText(task['duration'])
        self.pauseDuration.setText(task['pause'])
        self.message.setText(task['message'])

        return task

    def setTask(self, task):
        time=task['duration']
        print(time)
        hour=0
        if 'h' in time: 
            _time=time.split('h')
            hour=int(_time[0])
            time=_time[1]
        minute=0
        if 'm' in time: 
            _time=time.split('m')
            minute=int(_time[0])
            time=_time[1]
        second=0
        if 's' in time: second=int(time.split('s')[0])

        self.updateWorkEndTime(hour=hour, minute=minute, second=second)

        time=task['pause']
        hour=0
        if 'h' in time: 
            _time=time.split('h')
            hour=int(_time[0])
            time='None'
            if len(_time)>1: time=_time[1]
        minute=0
        if 'm' in time: 
            _time=time.split('m')
            minute=int(_time[0])
            time='None'
            if len(_time)>1: time=_time[1]
        second=0
        if 's' in time: second=int(time.split('s')[0])

        self.updateRestEndTime(hour=hour, minute=minute, second=second)

        self.updateMaxRepetitions(task['pomodoros'])

        self.taskLabel.setText(task['title'])
        self.pomodoroNumber.setText(str(task['pomodoros']))

    def saveTask(self):
        data=self.getData()
        data['tags']='regular'
        self.db.addTask(data)
        self.insertTasks()

    def makeIcon(self, name, end="png"):
        iconPath = QFileInfo(__file__).dir()
        iconPath.cd("data")
        iconPath.cd("icons")
        iconPath = iconPath.filePath(f"{name}.{end}")
        return QIcon(iconPath)

    def setupTrayicon(self):
        self.trayIcon = QSystemTrayIcon(self.makeIcon("tomato"))
        self.trayIcon.setContextMenu(QMenu())
        self.trayIcon.activated.connect(self.onActivate)
        self.trayIcon.show()

    def startTimer(self):
        if self.beginningStamp is None: self.beginningStamp=datetime.now()
        try:
            if not self.timer.isActive(): self.createTimer()
        except:
            self.createTimer()

    def createTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.timeout.connect(self.maybeChangeMode)
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.start()

    def pauseTimer(self):
        try:
            self.timer.stop()
            self.timer.disconnect()
        except:
            pass

    def resetTimer(self):
        try:
            self.pauseTimer()
            self.time = QTime(0, 0, 0, 0)
            self.displayTime()
        except:
            pass

    def maybeStartTimer(self):
        if self.currentRepetitions != self.maxRepetitions:
            self.startTimer()
            started = True
        else:
            self.currentRepetitions = 0
            started = False
            self.submitPomodoro()
        return started

    def updateWorkEndTime(self, hour, minute, second):
        self.workEndTime = QTime(hour, minute, second)

    def updateRestEndTime(self, hour, minute, second):
        self.restEndTime = QTime(hour, minute, second)

    def updateMaxRepetitions(self, value):
        self.maxRepetitions = 2*value

    def updateCurrentMode(self, mode: str):
        self.currentMode = Mode.work if mode == "work" else Mode.rest

    def updateTime(self):
        self.time = self.time.addSecs(1)
        self.totalTime = self.totalTime.addSecs(1)
        if self.modeComboBox.currentText() == "work":
            self.workTime = self.workTime.addSecs(1)
        else:
            self.restTime = self.restTime.addSecs(1)
        self.displayTime()

    def playSound(self, start=True):
        if start:
            audioFile='/home/adam/code/lura/lura/plugins/pomodoro/data/audio/start.wav'
        else:
            audioFile='/home/adam/code/lura/lura/plugins/pomodoro/data/audio/end.wav'
        player =QMediaPlayer()
        player.setMedia(QMediaContent(QUrl.fromLocalFile(audioFile)))
        player.setVolume(100)
        player.play()
        time.sleep(10)

    def maybeChangeMode(self):
        if self.currentMode is Mode.work and self.time >= self.workEndTime:
            self.resetTimer()
            self.modeComboBox.setCurrentIndex(1)
            self.incrementCurrentRepetitions()
            try:
                r=int(self.pomodoroNumber.text())
            except ValueError:
                pass
            self.pomodoroNumber.setText(str(r-1))
            started = self.maybeStartTimer()
            self.showWindowMessage(
                Status.workFinished if started else Status.repetitionsReached
            )
            self.playSound(start=False)
        elif self.currentMode is Mode.rest and self.time >= self.restEndTime:
            self.resetTimer()
            self.modeComboBox.setCurrentIndex(0)
            self.incrementCurrentRepetitions()
            started = self.maybeStartTimer()
            self.showWindowMessage(
                Status.restFinished if started else Status.repetitionsReached
            )
            self.playSound(start=True)

    def incrementCurrentRepetitions(self):
        if self.maxRepetitions > 0: self.currentRepetitions += 1

    def insertTasks(self):
        self.taskModel.clear()
        for task in self.db.tasks():
            item=QStandardItem('{}. {}'.format(task['id'], task['title']))
            item=QStandardItem(task['title'])
            item.m_id=task['id']
            self.taskModel.appendRow(item)

    def displayTime(self):
        self.timeDisplay.display(self.time.toString(self.timeFormat))

    def showWindowMessage(self, status):
        if status is Status.workFinished:
            self.trayIcon.showMessage(
                "Break", 'Take a break', self.makeIcon("tomato")
            )
        elif status is Status.restFinished:
            self.trayIcon.showMessage(
                "Work", 'Back to work', self.makeIcon("tomato")
            )
        else:
            self.trayIcon.showMessage(
                "Finished", 'Mission accomplished', self.makeIcon("tomato")
            )
            self.resetButton.click()

    def makeButton(self, text, iconName=None, disabled=True):
        button = QPushButton(text, sizePolicy=self.size_policy)
        if iconName:
            button.setIcon(self.makeIcon(iconName))
        button.setDisabled(disabled)
        return button

    def onActivate(self, reason):
        if reason == QSystemTrayIcon.Trigger: self.show()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Q:
            self.window.close()
