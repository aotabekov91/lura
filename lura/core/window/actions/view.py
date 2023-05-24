import os

from lura.utils import Plugin

class DocumentViewActions(Plugin):
    def __init__(self, app):
        super().__init__(app, name='navigation')

    def nextPage(self):
        self.app.window.view().nextPage()

    def previousPage(self):
        self.app.window.view().previousPage()

    def pageDown(self):
        self.app.window.view().pageDown()

    def pageUp(self):
        self.app.window.view().pageUp()

    def pageLeft(self):
        self.app.window.view().pageLeft()

    def pageRight(self):
        self.app.window.view().pageRight()

    def incrementUp(self):
        self.app.window.view().incrementUp()

    def incrementDown(self):
        self.app.window.view().incrementDown()

    def gotoEnd(self):
        last_page=self.app.window.view().document().numberOfPages()
        self.app.window.view().jumpToPage(last_page)

    def gotoBeginning(self):
        self.app.window.view().jumpToPage(1)
