import os
import hashlib
from gizmo.mixin import model
from PyQt5 import QtCore, QtGui

class DirElement(model.Dir):

    def setup(self):

        self.m_data = {} 
        self.m_loaded = {}
        super().setup()
        self.assignId()
        self.setFiles()

    def assignId(self):

        if os.path.exists(self.m_source):
            p=os.path.expanduser(self.m_source)
            p=os.path.abspath(p)
            self.m_source=p
            f=os.path.dirname(p)
            self.m_folder=f

    def loadImage(self, p):

        if p and not p in self.m_loaded:
            img=QtGui.QImage(p)
            size=QtCore.QSizeF(img.size())
            idx=self.assignIdentifier(p)
            data={
                'path': p,
                'img': img,
                'idx': idx,
                'size': size
                }
            self.m_loaded[p]=data
        return self.m_loaded.get(p)

    def assignIdentifier(self, source):

        if os.path.isfile(source):
            source=os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            return shash.hexdigest()

    def loadData(self, idx):

        p=self.m_data.get(idx)
        return self.loadImage(p)

    def load(self): 
        self.loaded.emit(self)

    def count(self):
        return len(self.m_data)

    def createElement(self):
        return self.element_class(model=self)
