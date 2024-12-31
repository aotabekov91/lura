import json
from plug import Plug

class StatePosition(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.connectAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.connectAgent)

    def connectAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        stater=self.app.plugman.getPlug('StatesTable')
        if normal and stater:
            normal.positionChanged.connect(self.savePosition)
            self.app.appIsLaunched.connect(self.setPosition)

    def savePosition(self, view, data):
        position=json.dumps(data)
        stater=self.app.plugman.getPlug('StatesTable')
        model=view.model()
        if model:
            midx=model.id()
            stater.setState(midx, 'position', position)

    def setPosition(self):
        views=self.app.buffman.views()
        normal=self.app.plugman.getPlug('Normal')
        stater=self.app.plugman.getPlug('StatesTable')
        for view in views:
            model=view.model()
            if model: 
                midx=model.id()
                data=stater.getState(midx, 'position')
                if data: 
                    data=data[0]
                    position_text=data['value'].replace("'", '"')
                    position=json.loads(position_text)
                    normal.activate(action='goTo', view=view, **position)
