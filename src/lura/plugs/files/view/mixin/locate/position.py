from gizmo import mixin

class PLocate(mixin.view.Locate):

    def openPositionLocator(self, data={}, **kwargs):
        
        path=data.get('position')
        print(path)
        if path: self.goTo(path=path)
        return path

    def getPositionLocator(self, data={}, **kwargs):

        idx=self.currentIndex()
        path=self.m_model.filePath(idx)
        data['position']=path
        return self.createLocator(data)
