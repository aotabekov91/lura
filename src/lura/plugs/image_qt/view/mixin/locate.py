from gizmo.mixin import view

class Locate(view.Locate):

    def getLocator(self, *args, **kwargs):

        kwargs['item']=self.currentItem()
        return super().getLocator(*args, **kwargs)
