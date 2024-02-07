import os
from plug import Plug
from gizmo.utils import tag

from .model import FileModel
from .view import FilesTab, FilesView

class FileBrowser(Plug):

    def setup(self):

        super().setup()
        h=self.app.ui.handler
        h.addViewer(FilesView)
        h.addModeller(FileModel)
        self.tab=FilesTab(
                app=self.app,
                label='FilesTab',
                identifier='FilesTab',
                )
        self.app.ui.uiman.locate(self.tab)
        self.app.ui.buffer.setFiller(
                'path', self.pathFiller)
        self.app.appLaunched.connect(
                self.initiateTab)

    def initiateTab(self):

        p=os.path.abspath('.')
        self.app.ui.handler.initiate(p)

    @tag(modes=['exec'], filler={'path': 'path'})
    def openFile(self, path):

        p=os.path.abspath(path)
        if os.path.exists(p):
            self.tab.activate()
            self.tab.current.goTo(path=p)

    def pathFiller(self, path=None):

        path = path or os.path.abspath('.')
        t=path.rsplit('/', 1)
        if len(t)==2:
            p, c = t[0]+'/', t[1] 
        else:
            p, c = '.', t[0] 
        clist=[]
        try:
            for i in os.listdir(p):
                if i[:len(c)]==c:
                    if p!='.':
                        i=os.path.join(p, i)
                    clist+=[i.replace(' ', '\ ')]
        except:
            pass
        finally:
            return clist
