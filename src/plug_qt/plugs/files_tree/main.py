import os
from PyQt6 import QtGui

from plug_qt import gizmo
from plug import tag, Plug, Model, Factory

class FilesTree(Plug):

    def setup(self):
        super().setup()
        self.setupView()
        self.setPath()

    def getPath(self, index=None):
        if not index: 
            index=self.view.currentIndex()
        if index:
            model=self.view.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def setPath(self, path=None):
        model=Factory(Model, QtGui.QFileSystemModel)()
        self.view.setModel(model)
        if path is None: 
            path = os.path.abspath('.')
        model.setRootPath(path)
        idx=model.index(path)
        self.view.setRootIndex(idx)
        for row in range(1, 4): 
            self.view.hideColumn(row)

    def setupView(self):
        self.view=self.app.buffman.createView(
                gizmo.TreeView, 
                name='FilesView', 
                attributes=[
                    {'key':'position', 'value':{"FilesView":"D|L"}}
                    ])

    @tag('<c-F>(normal/filestree)')
    def toggle(self):
        self.view.toggle()

    @tag('t(normal)[FilesView]')
    def openInTab(self, *args, **kwargs):
        new_tab=self.app.view.main.create()
        new_tab.activate()
        self.open(*args, **kwargs)

        # todo: heck who knows what is going on here?
        # view=self.app.stateman.subview()
        # tab_normal=self.app.plugman.getPlug('TabNormal')
        # if tab_normal:
        #     tview=tab_normal.activate(
        #             action='create', focus=True)#, view=view, focus=True)
        #     print(tview)
        #     # self.open(*args, **kwargs)

    @tag('T(normal)[FilesView]')
    def openInTabAndFocus(self, *args, **kwargs):
        kwargs['focus']=True 
        self.openInTab(*args, **kwargs)

    @tag('o(normal)[FilesView]')
    def open(self, focus=False, **kwargs):
        idx=self.view.currentIndex()
        path=self.getPath(idx)
        if path:
            if os.path.isdir(path): 
                self.view.expand(idx)
            else:
                self.app.buffman.open(source=path, **kwargs)
            if not focus:
                self.view.activate()

    @tag('O(normal)[FilesView]')
    def openAndFocus(self, *args, **kwargs):
        kwargs['focus']=True
        self.open(*args, **kwargs)
