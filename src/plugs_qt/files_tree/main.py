import os
from PyQt6 import QtGui

from plug import Plug, tag, Model

from .view import FilesView

class FileSystemModel(
        Model,
        QtGui.QFileSystemModel,
        ):
    pass

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
        files_model=FileSystemModel()
        self.view.setModel(files_model)
        if path is None: 
            path = os.path.abspath('.')
        files_model.setRootPath(path)
        idx=files_model.index(path)
        self.view.setRootIndex(idx)
        for row in range(1, 4): 
            self.view.hideColumn(row)

    def setupView(self):
        self.view=self.app.buffman.createView(
                FilesView, None)

    def updateOutline(self, view):
        model=view.model()
        name=model.__class__.__name__
        outliner=self.outliner(name)
        if outliner:
            outline=outliner.getOutline(model)
            if outline:
                self.view.setModel(outline)

    @tag('<c-F>(normal/filestree)')
    def toggleOutline(self):
        self.view.toggle()

    @tag('o(normal)[FilesView]')
    def open(self, focus=False):
        idx=self.view.currentIndex()
        path=self.getPath(idx)
        if path:
            if os.path.isdir(path): 
                self.view.expand(idx)
            else:
                self.app.buffman.open(source=path)
            if not focus:
                self.view.activate()
                #todo :current:
                # bug self.view.activate -> dock partial view shown

    @tag('O(normal)[FilesView]')
    def openAndFocus(self, *args, **kwargs):
        kwargs['focus']=True
        self.open(*args, **kwargs)
