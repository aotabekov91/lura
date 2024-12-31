import json
from plug import Plug

class StateZoom(Plug):

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
            normal.zoomChanged.connect(self.saveZoom)
            self.app.appIsLaunched.connect(self.setZoom)

    def saveZoom(self, view, data):
        model=view.model()
        stater=self.app.plugman.getPlug('StatesTable')
        if model:
            data=json.dumps(data)
            obj=model.id()
            stater.setState(obj, 'zoom', data)

    def setZoom(self):
        views=self.app.buffman.views()
        normal=self.app.plugman.getPlug('Normal')
        stater=self.app.plugman.getPlug('StatesTable')
        for view in views:
            model=view.model()
            if model:
                obj=model.id()
                data=stater.getState(obj, 'zoom')
                if data: 
                    data=data[0]
                    zoom_text=data['value'].replace("'", '"')
                    zoom=json.loads(zoom_text)
                    normal.activate(action='zoom', view=view, **zoom)
