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
        goer=self.app.plugman.plugs.get('Go')
        stater=self.app.plugman.plugs.get('StatesTable')
        if goer and stater:
            goer.positionChanged.connect(self.savePosition)
            self.app.appIsLaunched.connect(self.setPosition)

    def savePosition(self, view, data):
        position=json.dumps(data)
        stater=self.app.plugman.plugs.get('StatesTable')
        model=view.model()
        if model:
            obj=model.id()
            stater.setState(obj, 'position', position)

    def setPosition(self):
        views=self.app.buffman.views()
        goer=self.app.plugman.plugs.get('Go')
        stater=self.app.plugman.plugs.get('StatesTable')
        for view in views:
            model=view.model()
            if not model: continue
            obj=model.id()
            data=stater.getState(obj, 'position')
            if not data: continue
            data=data[0]
            position_text=data['value'].replace("'", '"')
            position=json.loads(position_text)
            goer.goTo(view, **position)
