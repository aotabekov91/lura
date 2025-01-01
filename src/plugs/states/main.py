import json

from PyQt6 import QtCore

from plug import Plug

class States(Plug):

    wait_time=500
    states=['zoom', 'goTo']

    def setup(self):
        super().setup()
        if self.app.running:
            self.setStates()
        else:
            self.app.appIsLaunched.connect(
                    self.setStates)

    def connectStates(self):
        normal=self.app.plugman.getPlug('Normal')
        stater=self.app.plugman.getPlug('StatesTable')
        if normal and stater:
            normal.stateChanged.connect(self.savePosition)

    def savePosition(self, state, view, data):
        if state in self.states:
            data=json.dumps(data)
            stater=self.app.plugman.getPlug('StatesTable')
            model=view.model()
            if model:
                midx=model.id()
                stater.setState(midx, state, data)

    def setStates(self):
        timer=QtCore.QTimer(parent=self.app.qapp)
        timer.singleShot(self.wait_time, self.waitAndSet)

    def waitAndSet(self):
        views=self.app.buffman.views()
        normal=self.app.plugman.getPlug('Normal')
        stater=self.app.plugman.getPlug('StatesTable')
        for view in views:
            model=view.model()
            if model: 
                midx=model.id()
                for state in self.states:
                    data=stater.getState(midx, state)
                    if data: 
                        data=data[0]
                        value=data['value'].replace("'", '"')
                        value=json.loads(value)
                        normal.activate(
                                action=state, view=view, **value)
        if not self.activated:
            self.activate()
            self.connectStates()
