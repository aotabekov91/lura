import os

from PyQt6 import QtWebEngineWidgets, QtWidgets

from plug_qt import vimo

class BrowserView(
        vimo.View,
        QtWidgets.QWidget,
):
    isSubview=True
    canFollow = True


    def setup(self):
        super().setup()
        self.m_browser=None
        self.setupBrowser()

    def setupBrowser(self):
        self.m_layout=QtWidgets.QBoxLayout()
        self.m_browser=QtWebEngineWidgets.QWebEngineView(self)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)

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
