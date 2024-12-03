import gizmo
from PyQt5 import QtCore

class SourceModel(
        gizmo.ui.qt.vimo.model.Model,
        QtCore.QAbstractListModel
        ):

    populated = QtCore.pyqtSignal(int)

    def setup(self):

        super().setup()
        self.m_root=''
        self.m_cache={}
        self.m_row_count=None

    def setMinimumRowCount(self, count=None):

        if count:
            c=self.getRootData(index=0)
            count=min(count, c) 
        self.m_row_count=count
        self.beginResetModel()
        self.endResetModel()

    def getRootData(
            self, 
            root=None, 
            index=None,
            ):

        root=root or self.m_root
        d=self.m_cache.get(root)
        if not d: d=0, True, None, [] 
        if index is None: return d
        return d[index]

    def rowCount(self, parent=None):

        if self.m_row_count: 
            return self.m_row_count
        return self.getRootData(index=0)

    def data(
            self, 
            idx, 
            role=QtCore.Qt.DisplayRole,
            root=None,
            **kwargs,
            ):

        c, f, p, alist=self.getRootData(root)
        if not idx.isValid():
            return None
        elif idx.row()<0:
            return None
        elif idx.row() >= c:
            return None
        elif role == QtCore.Qt.DisplayRole:
            return alist[idx.row()]

    def canFetchMore(
            self, index=None, root=None):

        return self.getRootData(root, index=1)

    def fetchMore(
            self, 
            index=None, 
            limit=100,
            root=None,
            ):

        root=root or self.m_root
        if not root: return

        c, f, ipath, alist=self.getRootData(
                root=root)
        start=c
        for i in range(limit): 
            if not ipath.hasNext(): 
                f=False
                break
            p=ipath.next()
            p=p.replace(self.m_root, '', 1)
            alist+=[p]
            c+=1
        data=(c, f, ipath, alist)
        self.m_cache[self.m_root]=data

        if self.m_root==root:
            idx=QtCore.QModelIndex()
            self.beginInsertRows(idx, start, c) 
            self.endInsertRows()
            self.populated.emit(c-start)

    def setRootPath(self, path):

        self.beginResetModel()
        if not path.endswith('/'): 
            path+='/'
        self.m_root=path
        if not path in self.m_cache:
            flags=QtCore.QDir.AllDirs
            flags=flags|QtCore.QDir.NoDotAndDotDot
            options=QtCore.QDirIterator.Subdirectories
            options=options|QtCore.QDirIterator.FollowSymlinks
            ipath=QtCore.QDirIterator(
                    path, flags, options)
            d=0, True, ipath, []
            self.m_cache[path]=d
        c, f, path, alist=self.getRootData()
        self.m_count=c
        self.m_path=path
        self.m_can_fetch=f
        self.m_file_list=alist
        self.endResetModel()
