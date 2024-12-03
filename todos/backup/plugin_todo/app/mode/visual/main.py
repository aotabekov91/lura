from ..base import Mode 

class Visual(Mode):

    def __init__(self, 
                 app,
                 listen_leader='#',
                 show_statusbar=True,
                 delisten_on_exec=False,
                 ):

        super().__init__(app, 
                         listen_leader=listen_leader,
                         show_statusbar=show_statusbar,
                         delisten_on_exec=delisten_on_exec,
                         )

        self.hints=None
        self.hinting=False

    def activateCheck(self, event):

        leaderPressed=super().activateCheck(event)
        if leaderPressed:
            return self.app.modes.normal.listening
