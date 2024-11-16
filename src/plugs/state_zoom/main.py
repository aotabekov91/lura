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
        zoomer=self.app.plugman.plugs.get('Zoom')
        stater=self.app.plugman.plugs.get('StatesTable')
        if zoomer and stater:
            zoomer.zoomChanged.connect(self.saveZoom)
            self.app.appIsLaunched.connect(self.setZoom)

    def saveZoom(self, view, data):
        data=json.dumps(data)
        stater=self.app.plugman.plugs.get('StatesTable')
        model=view.model()
        if model:
            obj=model.id()
            stater.setState(obj, 'zoom', data)

    def setZoom(self):
        views=self.app.buffman.views()
        zoomer=self.app.plugman.plugs.get('Zoom')
        stater=self.app.plugman.plugs.get('StatesTable')
        for view in views:
            model=view.model()
            if not model: continue
            obj=model.id()
            data=stater.getState(obj, 'zoom')
            if not data: continue
            data=data[0]
            zoom_text=data['value'].replace("'", '"')
            zoom=json.loads(zoom_text)
            zoomer.zoomTo(view, **zoom)
