from qplug.utils import register
from qplug.modes import Command as Mode

class Command(Mode):

    @register('sp')
    def splitHorizontally(self):

        view=self.app.main.display.view
        if view:
            filePath=view.model().filePath()
            pageNumber=view.currentPage()
            left, top =view.saveLeftAndTop()
            self.app.main.open(filePath)
            self.app.main.display.view.goto(pageNumber, left, top)
