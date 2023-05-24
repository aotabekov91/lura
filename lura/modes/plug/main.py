from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Mode

class Plug(Mode):

    def __init__(self, app):

        super(Plug, self).__init__(app=app, 
                                   name='plug', 
                                   show_statusbar=True,
                                   show_commands=False,
                                   delisten_on_exec=False,
                                   )
