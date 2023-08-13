from qplug.utils import register
from qplug.modes import Normal as Mode

class Normal(Mode):

    @register(key='yy')
    def yank(self):

        view=self.app.main.display.view
        if view and view.selected(): 
            text=[]
            for s in view.selected(): text+=[s['text']]
            text=' '.join(text)
            self.app.clipboard().setText(text)
            view.select()

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
