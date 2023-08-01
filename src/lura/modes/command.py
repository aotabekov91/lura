from qapp.utils import register
from qapp.app.mode import Command as Mode

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
