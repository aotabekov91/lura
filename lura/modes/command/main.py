from lura.utils import Mode

class Command(Mode):

    def __init__(self, app):

        super(Command, self).__init__(app=app, 
                                      name='command',
                                      listen_leader=',',
                                      show_commands=True, 
                                      show_statusbar=True,
                                      )
