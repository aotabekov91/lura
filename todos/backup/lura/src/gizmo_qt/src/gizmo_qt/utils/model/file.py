from os.path import abspath

from PyQt6.QtGui import QFileSystemModel

from .base import Model


class FileSystemModel(Model, QFileSystemModel):
    root_path = "/"

    def id(self):
        if not self.m_id:
            return self.rootPath()
        return self.m_id

    def setup(self):
        super().setup()
        self.setRootPath(self.root_path)

    def getPathIndex(self, path=None):
        path = path or abspath(".")
        return self.index(path)

    def element(self, idx):
        return self.filePath(idx)
