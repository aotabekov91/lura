from plugin.app import register
from plugin.app.mode import Normal as Mode

class Normal(Mode):

    @register(key='w')
    def fitToPageWidth(self): 

        view=self.app.main.display.view
        if view: view.fitToPageWidth()

    @register(key='s')
    def fitToPageHeight(self): 

        view=self.app.main.display.view
        if view: view.fitToPageHeight()

    @register(key='c')
    def toggleContinuousMode(self): 

        view=self.app.main.display.view
        if view: view.toggleContinuousMode()

    @register('C')
    def cleanUp(self): 

        view=self.app.main.display.view
        if view: view.cleanUp()
