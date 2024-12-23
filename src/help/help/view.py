import os
from PyQt6 import QtWebEngineWidgets, QtCore

from plug_qt import vimo

class HelpView(
    vimo.View,
    QtWebEngineWidgets.QWebEngineView,
):
    isSubview=True
    canFollow = True
    position = {"HelpView": "C|x"}

    def setup(self):
        super().setup()
        self.m_model=None
        self.m_current=None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setContentsMargins(3, 3, 3, 3)
        self.app.appIsLaunched.connect(self.text)

    def setModel(self, model):
        if id(self.m_model) != id(model):
            html=model.modelData()
            base=QtCore.QUrl.fromLocalFile(os.getcwd()+os.path.sep)
            self.setHtml(html, baseUrl=base)

    def text(self):
        page=self.page()
        print(page.toHtml())

    def count(self):
        return 100

    def currentIndex(self):
        # todo in %
        return self.m_current

    def setCurrentIndex(self, idx):
        if self.m_current != idx:
            current, previous = idx, self.m_current
            self.m_current, self.m_previous = current, previous
        self.indexChanged.emit(self.m_current)
