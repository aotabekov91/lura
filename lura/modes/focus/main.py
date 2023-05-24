from lura.utils import Mode
from functools import partial

class Focus(Mode):

    def __init__(self, app):

        super(Focus, self).__init__(app=app, 
                                      name='follow',
                                      listen_leader='!',
                                      show_commands=True, 
                                      show_statusbar=True,
                                      )

    def setData(self):

        self.commands=[]

        self.setDocks()
        self.setViews()

        self.commands=sorted(self.commands, key=lambda x: x['down'])
        self.ui.mode.setList(self.commands)

    def setDocks(self):

        for position in ['right',  'left', 'top', 'bottom']:
            dock=getattr(self.app.window.docks, position)
            current=dock.current()
            if dock.isVisible() and current:
                key=f'd{position[0]}'
                self.commands+=[{'up': current.plugin.name, 
                                 'down':key, 
                                 'id':dock.setFocus}]

    def setViews(self): 

        for i, view in self.app.window.display.views.items():
            self.commands+=[{'up':view.document().filePath(),
                             'down':f'v{i+1}',
                             'id':partial(self.focusView, view)}]

    def focusView(self, view):

        view.setFocus()
        self.app.window.display.setCurrentView(view)
        self.delistenWanted.emit()

    def _onExecuteMatch(self):

        self.delisten()

    def _getFunc(self, data):

        return data['id']

    def listen(self):

        self.setData()
        super().listen()
