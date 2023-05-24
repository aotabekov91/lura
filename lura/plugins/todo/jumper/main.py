from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin

class PageJumper(Plugin):

    def __init__(self, app):

        super(PageJumper, self).__init__(app)

        self.always_listen=True
        self.listen_widget=self.app.window
        self.app.installEventFilter(self)

    def goto(self, digit=1):

        self.app.window.display.view.jumpToPage(digit)

    def gotoEnd(self):

        document=self.app.window.display.view.document()
        self.app.window.display.view.jumpToPage(document.numberOfPages())

    def gotoBegin(self):

        self.app.window.display.view.jumpToPage(1)
