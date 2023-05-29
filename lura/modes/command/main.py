from lura.utils import Mode
from .widget import CommandWindow 

class Command(Mode):

    def __init__(self, app):

        super(Command, self).__init__(app=app, 
                                      name='command',
                                      listen_leader=',',
                                      show_commands=True, 
                                      show_statusbar=True,
                                      )

    def setUI(self):
        
        self.ui=CommandWindow(self.app)

        self.ui.mode.hideWanted.connect(self.deactivate)
        self.ui.mode.returnPressed.connect(self.confirm)
        self.ui.mode.installEventFilter(self)
