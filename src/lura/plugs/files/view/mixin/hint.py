from gizmo import mixin
from PyQt5 import QtWidgets, QtCore

class Hint(mixin.view.Hint):

    labels={}
    canSelect=True

    def hint(self):

        self.m_hinting=True
        alist = self.getRows()
        if alist:
            self.m_map=self.generate(alist)
            self.updateHintItems()
        else:
            self.hintFinished.emit()
            self.cleanUpHinting()

    def getRows(
            self, 
            root=None, 
            model=None, 
            alist=[]
            ):

        if not root:
            model=self.m_model
            path=model.rootPath()
            root=model.getPathIndex(path)
        for r in range(model.rowCount(root)):
            c = root.child(r, 0)
            alist+=[c]
            if model.rowCount(c):
                self.getRows(c, model, alist)
        return alist

    def generate(self, alist):

        hmap = {} 
        for j, d in enumerate(alist):
            r=self.visualRect(d)
            if r.isValid():
                i=self.currentItem(d)
                m=str(j+1)
                hmap[m]={
                        'box': r, 
                        'item': i,
                        'index': d, 
                        }
        return hmap

    def updateHint(self, key=''):

        match={}
        for k, l in self.m_map.items():
            if key==k[:len(key)]:
                match[k]=l
        if len(match)==0:
            self.hintFinished.emit()
            self.cleanUpHinting()
            self.disconnectHint()
        elif len(match)==1:
            d=match[list(match.keys())[0]]
            self.hintSelected.emit(d)
            self.cleanUpHinting()
            self.disconnectHint()
        else:
            self.m_map=match
            self.updateHintItems()

    def cleanUpHinting(self):

        for i in self.labels.values():
            i.hide()
        self.labels={}
        super().cleanUpHinting()

    def updateHintItems(self):

        for n, d in self.m_map.items():
            l=QtWidgets.QLabel(
                    n,
                    parent=self,
                    objectName='HintLabel',
                    )
            r=d['box']
            self.labels[n]=l
            l.setAlignment(QtCore.Qt.AlignRight)
            l=self.labels[n]
            x, y = r.x(), r.y()
            w, h = r.width(), r.height() 
            l.setGeometry(x, y, w, h)
            l.show()

    def select(self, item, sel):

        idx=sel.get('index', None)
        if idx: self.setCurrentIndex(idx)
