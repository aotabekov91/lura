from lura.utils import Mode
from functools import partial

class Focus(Mode):

    def __init__(self, app):

        super(Focus, self).__init__(app=app, 
                                    name='focus', 
                                    listen_leader='f', 
                                    show_commands=True, 
                                    show_statusbar=True,
                                    delisten_wanted='plug',
                                    )
