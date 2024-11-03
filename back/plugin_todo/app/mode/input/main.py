from ..base import Mode

class Input(Mode):

    def __init__(self, app):

        super().__init__(app=app, 
                         listen_leader='@', 
                         show_statusbar=True,
                         delisten_on_exec=False,
                         )
