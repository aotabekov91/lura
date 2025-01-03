import os
import re
import markdown

from PyQt6 import QtCore

import plug_qt

from .utils import UrlizeExtension

class HelpModel(
    plug_qt.vimo.model.Model,
    QtCore.QObject,
):
    kind = "HELP"
    theme='default'
    pattern = ".*help.md$"
    wantView = ["HelpView"]

    modelUpdated = QtCore.pyqtSignal()
    loaded = QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_themes={}
        self.m_data=None
        self.m_theme=None
        self.m_converter=None
        self.assignId(self.m_source)

    def load(self):
        if not self.isLoaded:
            md, data = self.loadMD(self.m_source)
            self.m_data=data
            self.m_converter = md
            self.isLoaded = True

    def converter(self):
        return self.m_converter

    def loadMD(self, source):
        with open(source, 'r') as file:
            contents = file.read()
            extensions = [
                'toc',
                'tables',
                'fenced_code',
                'pymdownx.tilde',
                'pymdownx.tasklist',
                UrlizeExtension(),
            ]
            md = markdown.Markdown(extensions=extensions)
            return md, md.convert(contents)

    def assignId(self, source):
        if os.path.isfile(source):
            self.setId(source)

    @classmethod
    def isCompatible(cls, source, **kwargs):
        if type(source) != str:
            return
        if not cls.pattern:
            return
        if not os.path.exists(source):
            return
        return re.match(cls.pattern, source, re.I)
