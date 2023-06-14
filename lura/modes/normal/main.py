from lura.utils import Mode

class Normal(Mode):

    def __init__(self, app):

        super(Normal, self).__init__(app=app, 
                                     name='normal',
                                     listen_leader='@',
                                     show_commands=False,
                                     delisten_on_exec=False,
                                    )
