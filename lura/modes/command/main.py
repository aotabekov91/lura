from plugin.app import register
from plugin.app.mode import Command as Mode

class Command(Mode):

    @register('wsp')
    def splitHorizontally(self):

        view=self.app.main.display.view
        if view:
            filePath=view.model().filePath()
            pageNumber=view.currentPage()
            left, top =view.saveLeftAndTop()
            self.app.main.open(filePath)
            self.app.main.display.view.goto(pageNumber, left, top)
