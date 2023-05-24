from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin

from .jumpers import ViewJumper
from .jumpers  import DockJumper

class Jumper(Plugin):

    def __init__(self, app):

        super(Jumper, self).__init__(app)

        self.dock_jumper=DockJumper(app)
        self.view_jumper=ViewJumper(app)
